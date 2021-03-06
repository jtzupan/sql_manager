/*
SUMMARY: This is a simple query to do several things<end>
KEYWORDS: LOLA, ZING, QUICKHIT, TEST<end>

*/


--select everyone who received an zing email on 4/30/16
--matches back to LOLA on email address

SELECT rs.EmailAddress
		,l.email
		,l.jacketnumber
		,l.CreateDtID

		into bisandboxwrite..zupan_zing_quickhit
   
  FROM [SRCMarketing].[dbo].[ResponsysSent] rs
		join qlods..lola l (NOLOCK) on l.email = rs.emailaddress
  where rs.campaignid = '100211762'
  AND rs.launchid = '100123335'
