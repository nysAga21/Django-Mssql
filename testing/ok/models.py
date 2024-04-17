from django.db import models




class Profile(models.Model):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s Profile"
    
class LinkRequests(models.Model):
    STATUS=(
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    )
    tin = models.CharField(max_length=100)
    issuerid = models.CharField(max_length=100)
    account_type =models.CharField(max_length=100)
    status=models.CharField(max_length=10,choices=STATUS,default='pending')
    accounts = models.TextField() 

    def save_accounts(self, accounts_list):
        self.accounts = ','.join(accounts_list)

    def get_accounts(self):
        return self.accounts.split(',')
    
    def __str__(self):
        return self.issuerid
    