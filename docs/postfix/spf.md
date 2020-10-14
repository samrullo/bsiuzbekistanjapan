# SPF (Sender Policy Framework)

Because SMTP doesn't have authentication mechanism, one can 
send email with any made up address.
As a result gmail smtp servers put such email in spam folder.

SPF record tells the recipient SMTP server that emails coming from you
are actually coming from you. It says to recipient 
go ahead and check that your IP address is authorized 
to send email from your domain thereby validating itself.

# how to set up SPF record
In DNS Advanced records.
```a mx``` means authorize my IP address.
```include:_spf.google.com``` means you are routing your emails through gmail SMTP, so you want to validate gmail as well.
```-all``` causes recipient server to reject anything else.
```~all```causes recipient server to accept but mark it as suspicious.

```python
type: TXT
Host: @(for all senders)
TXT value : v=spf1 a mx include:_spf.google.com -all
```
