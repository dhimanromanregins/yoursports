from django.contrib import admin
from .models import CustomUser, Pricing, Contact,PasswordResetToken, FootballTeam,FAQ, EndUser, EndUserDetail

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Pricing)
admin.site.register(Contact)
admin.site.register(PasswordResetToken)
admin.site.register(FootballTeam)
admin.site.register(FAQ)
admin.site.register(EndUser)
admin.site.register(EndUserDetail)

