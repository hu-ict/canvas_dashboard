
$ClientID = "184f1b4a-c0fe-4a81-b680-5eab8c90eeb0"
$TenantID = "98932909-9a5a-4d18-ace4-7236b5b5e11d"
$RedirectURI = "https://localhost"
$tenantname = "hogeschoolutrecht.onmicrosoft.com"


$students = import-csv c:\temp\Students.csv
$Tasklist = import-csv C:\temp\Tasks.csv
$BucketList = $Tasklist.Bucketname |select -Unique
$Categories = $Tasklist.Category |select -Unique

#Prepare Json for Categories and write ID to Tasklist
$i=0
$CategoriesJson = @"
{
    "categoryDescriptions": {
        $($Categories|foreach {
            $i++
            $cat = $_
            $Tasklist|foreach {If($_.Category -eq "$($cat)"){$_.CategoryId = $i}}
            "`"category$($i)`":`"$_`","+ [System.Environment]::NewLine})
    }
}
"@

#App login
$Response = Get-MsalToken -DeviceCode -ClientId $clientID -TenantId $tenantID -RedirectUri $RedirectURI
$headers = @{
    "Authorization" = "Bearer $($Response.AccessToken)"
    "Content-type"  = "application/json"
}

# ID of MS Team team
$GroupID = $students.TeamID |select -Unique


#Loop foreach student
Foreach($student in $students){

    #Add student to Team
    $body =@{
        "@odata.type" = "#microsoft.graph.aadUserConversationMember"
        "roles" = @("member")
        "user@odata.bind" = "https://graph.microsoft.com/v1.0/users/$($student.name)"
    }|ConvertTo-Json

    $URL = "https://graph.microsoft.com/v1.0/teams/$($GroupID)/members"
    $student = Invoke-RestMethod -Headers $headers -Uri $URL -Method POST -Body $body

#add channel for student in Class Team
    $BodyJsonChannel = @"
        {    
            "displayName":"$($student.displayname)",
            "description":"persoonlijk kanaal $($student.displayname)",
            "membershipType":"Standard"    
        }
"@

    $URL = "https://graph.microsoft.com/v1.0/teams/$($groupID)/channels" 
    $Channel = Invoke-RestMethod -Headers $headers -Uri $URL -Method POST -Body $BodyJsonChannel
    $ChannelID = $channel.id


    #Create Planner Plan for student
    $createPlanJSON = @"
        { 
	        "owner": "$($groupID)", 
	        "title": "Planner - $($student.displayname)" 
        }
"@

    $createPlanUri ="https://graph.microsoft.com/v1.0/planner/plans"
    $planResponse = Invoke-RestMethod -Method Post -Uri $createPlanUri -Headers $headers -Body $createPlanJSON
    $planID = $planResponse.id

    #Edit Plan categories
    $URL = "https://graph.microsoft.com/beta/planner/plans/$($planID)/details"
    $headers = @{
        "Authorization" = "Bearer $($Response.AccessToken)"
        "Content-type"  = "application/json"
    }
    $plandetails = Invoke-RestMethod -Method Get -Uri $URL -Headers $headers


    $URL = "https://graph.microsoft.com/v1.0/planner/plans/$planID/details"
    $headers = @{
        "Authorization" = "Bearer $($Response.AccessToken)"
        "Content-type"  = "application/json"
        "If-Match"      = "$($plandetails."@odata.etag")"
    }


    $Body = $CategoriesJson
    
    Invoke-RestMethod -Method Patch -Uri $URL -Headers $headers -Body $body

    #Redefine Headers
    $headers = @{
    "Authorization" = "Bearer $($Response.AccessToken)"
    "Content-type"  = "application/json"
}
    ## add some planner buckets
    Foreach($Bucket in $BucketList){
        $bucketJSON = @"
        {
          "name": "$($Bucket)",
          "planId": "$($planID)",
          "orderHint": " !"
        }
"@

        $bucketURI = "https://graph.microsoft.com/v1.0/planner/buckets"
        $graphResponse = Invoke-RestMethod -Method Post -Uri $BucketUri -Headers $headers -Body $BucketJSON
        $BucketID = $graphResponse.id
        $Tasklist | foreach {If ($_.Bucketname -eq $Bucket){$_.BucketId = $BucketID}}

    }

    Foreach($task in $Tasklist){
        If($task.DueDate){
            $DueDate = [System.Environment]::NewLine + "`"dueDateTime`":`"$($task.DueDate)`","
        }Else{
            $DueDate = $null
        }
        ## Add a Task
        $taskJSON = @"
        {
          "title": "$($task.TaskName)",
          "planId": "$($planID )",
          "bucketId" : "$($task.BucketId)",
          "orderHint": " !",
          "priority" : 5,$($DueDate)
          "appliedCategories": {
            "category$($task.CategoryId)": true
          },
          "assignments": {
              "$($student.userId)": {
              "@odata.type": "#microsoft.graph.plannerAssignment",
              "orderHint": " !",
              }
          }
        }
"@

        $taskURI = "https://graph.microsoft.com/beta/planner/tasks"
        $graphResponse = Invoke-RestMethod -Method Post -Uri $TaskUri -Headers $headers -Body $TaskJSON
        $taskID = $graphResponse.id
    }

    #Add Planner to Teams channel tab
    $tabsURI = "https://graph.microsoft.com/beta/teams/$($groupID)/channels/$($ChannelID)/tabs"
    $planURL = "https://tasks.office.com/$($tenantname)/Home/PlannerFrame?page=7&planId=$($planID)"

    $plannerJSON = @"
     {
	    "name": "$($student.displayname) - Planbord",
	    "displayName": "$($student.displayname) - Planbord",
        "teamsAppId" : "com.microsoft.teamspace.tab.planner",
        "configuration": {
            "entityId": "$($planID)",
		    "contentUrl": "$($planURL)",
		    "removeUrl": "$($planURL)",
		    "websiteUrl": "$($planURL)"
        }
    }
"@
        
    #Write-Host $plannerJSON
    $graphResponse = Invoke-RestMethod -Method Post -Uri $tabsURI -Headers $headers -Body $plannerJSON

}

############### CODE to Create private channel##########
<#

    $BodyJsonChannel = @"
        {
  "@odata.type": "#Microsoft.Graph.channel",
  "membershipType": "private",
  "displayName": "Private Channel DJ",
  "description": "This is my first private channels",
  "members":
     [
        {
           "@odata.type":"#microsoft.graph.aadUserConversationMember",
           "user@odata.bind":"https://graph.microsoft.com/v1.0/users('voornaam.achternaam@hu.nl')",
           "roles":["owner"]
        }
     ]
}
"@

$URL = "https://graph.microsoft.com/v1.0/teams/$($groupID)/channels" 
    $Channel = Invoke-RestMethod -Headers $headers -Uri $URL -Method POST -Body $BodyJsonChannel
    $ChannelID = $channel.id

    #>