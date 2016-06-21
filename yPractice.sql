SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED

/*
SUMMARY: this is all new <end>
KEYWORDS: purchase, closing, 2016<end>
*/


select lk.LoanNumber 
from qlods..lkwd lk
where lk.closingid > 20160101
and lk.loanpurposeid = 6