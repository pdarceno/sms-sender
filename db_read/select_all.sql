DECLARE @AsAtDate DATETIME = 	
CASE WHEN DATEPART(weekday, GETDATE()) BETWEEN 3 AND 6 THEN DATEADD(day, -1, GETDATE())	
     WHEN DATEPART(weekday, GETDATE()) BETWEEN 1 AND 2 THEN DATEADD(day, -3, GETDATE()) 	
     WHEN DATEPART(weekday, GETDATE()) = 7 THEN DATEADD(day, -2, GETDATE()) 	
END

SELECT
  L.Account# AS [{account_no_col}],
  dbo.GetBorrowersOfLoan(L.LoanAccountNumber, '; ', ' G') AS [{customer_name_col}],
  dbo.GetLoanPhoneNumbers(L.LoanAccountNumber, 'L', '; ', '############') AS [{phone_col}],
  dbo.GetLoanPhoneNumbers(L.LoanAccountNumber, 'G', '; ', '############') AS [{phone2_col}],
  L.BusinessCode AS [{business_code_col}],
  AB.ArrearsBalance AS [{arrears_balance_col}]
FROM FM_Loans L
OUTER APPLY dbo.GetBorrowerDetails(L.LoanAccountNumber) det
OUTER APPLY DBO.GetArrearsBalanceBaseTable(L.LoanAccountNumber, @AsAtDate, 1) AB	
WHERE L.Account# IN ({account_numbers_placeholder})
