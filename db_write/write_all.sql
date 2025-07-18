SET NOCOUNT ON
 
IF OBJECT_ID('tempdb..#LoanList') IS NOT NULL
	DROP TABLE #LoanList
 
--<< Change this to 0 when you want to generate the diary notes.>>--
--<< Dont run it against a live db until it has been tested >>--
Declare @TrialRun bit = 0
 
--Select accounts to be updated
Select LoanAccountNumber, Account#
Into #LoanList
From FM_Loans 
Where Account# IN (?);
 
Declare @Lan Integer
Declare @DateEntered Date = ?
Declare @DiaryReminderText NVARCHAR(MAX) = 'Sent SMS to customer - ' + ?

--Display list of accounts to be processed
Select * from #LoanList
 
--Insert the diary note.
SET @Lan = -1
If @TrialRun <> 1 
Begin
	WHILE @Lan IS NOT NULL
	BEGIN
	SELECT @Lan = MIN(LoanAccountNumber)
	FROM #LoanList
	WHERE LoanAccountNumber > @Lan
 
	IF @@ROWCOUNT <= 0 OR @Lan IS NULL
	BREAK
	INSERT INTO FM_DiaryReminders 
			([LoanAccountNumber],
			[DiaryReminderText],
			[DateEntered],
			[WhoEntered])
		Values
			(@Lan,
			@DiaryReminderText,
			@DateEntered,
			'SYS')
	END
END
 
Drop table #LoanList