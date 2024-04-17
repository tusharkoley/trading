from django.db import models

# Create your models here.
class Investement_Types(models.Model):
    description = models.CharField(unique=True, max_length=50)
    

class Sector(models.Model):
    decsription = models.CharField(unique=True, max_length=50)

class Stocks(models.Model):

    ticker = models.CharField(unique=True,max_length=50)
    company_name = models.CharField(max_length=50)
    comppany_description = models.TextField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    cap_typd = models.CharField(max_length=50)

class Shareholder_Patterns(models.Model):
    ticker = models.ForeignKey(Stocks,on_delete=models.CASCADE)
    shareholder_type = models.CharField(max_length=50)
    month = models.IntegerField()
    year = models.IntegerField()
    pct_holdings = models.FloatField()

class Stock_Price(models.Model):
    ticker = models.ForeignKey(Stocks,on_delete=models.CASCADE)
    date = models.DateField(null=False)
    open = models.FloatField(null=False)
    close = models.FloatField(null=False)
    high = models.FloatField()
    low = models.FloatField()
    volume = models.IntegerField()


class Fundamental_Data(models.Model):

    ticker = models.ForeignKey(Stocks,on_delete=models.CASCADE)
    revenue = models.FloatField()
    cost = models.FloatField()
    tax = models.FloatField()
    asset = models.FloatField()
    debt = models.FloatField()
    profit_after_tax = models.FloatField()
    total_share_outstanding = models.IntegerField()
    earninbgs_per_share = models.FloatField()
    book_value = models.FloatField()
    price = models.FloatField()
    date = models.DateField()
    operating_cost = models.FloatField()









