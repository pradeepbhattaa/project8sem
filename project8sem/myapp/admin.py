from django.contrib import admin
from .models import Test
from .models import UserRegistration
from .models import UserProfile
from .models import EmailVerification
from .models import KycRegistration
from .models import CandidateProfile
from .models import Notice
from .models import Kycverified
from .models import KycRequest
from .models import KycRejected
from .models import ProfilePicture
from .models import MpVote
from .models import MayorVote
from .models import DeputymayorVote
from .models import WardVote
from .models import VoteStatus



class TestAdmin(admin.ModelAdmin):
    list_display = ('email',)  # Display email in the admin list view

admin.site.register(Test, TestAdmin)


admin.site.register(UserProfile)
admin.site.register(EmailVerification)
admin.site.register(KycRegistration)
admin.site.register(CandidateProfile)
admin.site.register(Notice)
admin.site.register(Kycverified)
admin.site.register(KycRequest)
admin.site.register(KycRejected)
admin.site.register(ProfilePicture)
admin.site.register(MpVote)
admin.site.register(MayorVote)
admin.site.register(DeputymayorVote)
admin.site.register(WardVote)
admin.site.register(VoteStatus)








class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'middlename', 'lastname', 'phonenumber', 'email', 'date_of_birth')
    search_fields = ('firstname', 'lastname', 'email')
    list_filter = ('date_of_birth',)

admin.site.register(UserRegistration, UserRegistrationAdmin)





