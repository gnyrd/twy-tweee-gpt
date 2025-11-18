-- Export newsletters from Mail.app to .eml files
-- Instructions:
-- 1. In Mail.app, select the mailbox containing your newsletters
-- 2. Update the mailboxName variable below to match your mailbox
-- 3. Run: osascript export_newsletters_from_mail.scpt

set outputFolder to (path to home folder as text) & "Repos:TWEEE_gpt:sources:newsletters_eml:"
set accountName to "jpgan6"
set mailboxName to "TWY Newsletters"

tell application "Mail"
	-- Get the mailbox from specific account
	set theAccount to account accountName
	set theMailbox to mailbox mailboxName of theAccount
	set theMessages to messages of theMailbox
	set messageCount to count of theMessages
	
	log "Found " & messageCount & " messages in " & mailboxName
	
	-- Create output folder if needed
	tell application "Finder"
		if not (exists folder outputFolder) then
			make new folder at (path to home folder) with properties {name:"newsletters_eml"}
		end if
	end tell
	
	repeat with i from 1 to messageCount
		set theMessage to item i of theMessages
		set messageSubject to subject of theMessage
		set messageDate to date received of theMessage
		
		-- Clean filename (remove special characters)
		set cleanSubject to my replaceText(messageSubject, "/", "-")
		set cleanSubject to my replaceText(cleanSubject, ":", "-")
		set cleanSubject to my replaceText(cleanSubject, "?", "")
		
		-- Format: YYYY-MM-DD_Subject.eml
		set dateStr to (year of messageDate as string) & "-" & my zeroPad(month of messageDate as integer) & "-" & my zeroPad(day of messageDate)
		set fileName to dateStr & "_" & cleanSubject & ".eml"
		set outputPath to outputFolder & fileName
		
		-- Export as .eml
		try
			set emlData to source of theMessage
			set fileRef to open for access file outputPath with write permission
			set eof fileRef to 0
			write emlData to fileRef
			close access fileRef
			log "Exported: " & fileName
		on error errMsg
			log "Error exporting message " & i & ": " & errMsg
			try
				close access file outputPath
			end try
		end try
	end repeat
	
	log "Export complete! " & messageCount & " messages saved to newsletters_eml/"
end tell

-- Helper function to replace text
on replaceText(theText, findStr, replaceStr)
	set AppleScript's text item delimiters to findStr
	set textItems to text items of theText
	set AppleScript's text item delimiters to replaceStr
	set theText to textItems as text
	set AppleScript's text item delimiters to ""
	return theText
end replaceText

-- Helper function to zero-pad numbers
on zeroPad(num)
	if num < 10 then
		return "0" & num
	else
		return num as string
	end if
end zeroPad
