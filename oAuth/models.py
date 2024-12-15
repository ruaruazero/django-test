from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, user_phone, password=None, member_id=None, **extra_fields):
        """
        创建一个用户实例
        """
        if member_id is None:
            user_counts = User.objects.count()
            now = datetime.now()
            current_year = now.year % 100
            mid = '0' * (3 - user_counts // 10) + str(user_counts + 1)
            member_id = f'XY-{current_year}-{mid}'
        if not user_phone:
            raise ValueError(_('用户必须有一个手机号'))
        user = self.model(
            id=member_id,
            user_phone=user_phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_phone, password=None, **extra_fields):
        """
        创建一个超级用户实例
        """
        user_counts = User.objects.count()
        now = datetime.now()
        current_year = now.year % 100
        mid = '0' * (3 - user_counts // 10) + str(user_counts + 1)
        member_id = f'XY-{current_year}-{mid}'
        extra_fields.setdefault('is_member', 0)
        extra_fields.setdefault('is_staff', 0)
        extra_fields.setdefault('roles', 0)  # 假设0为管理员角色

        if extra_fields.get('is_staff') != 0:
            raise ValueError(_('超级用户必须有is_staff=True。'))
        if extra_fields.get('roles') != 0:
            raise ValueError(_('超级用户必须有roles=0。'))

        return self.create_user(user_phone, password, member_id, **extra_fields)



# Create your models here.
class User(AbstractBaseUser):

    role_type = [
        [0, 'admin'],
        [1, 'user']
    ]
    gender_type = [
        [0, 'male'],
        [1, 'female']
    ]
    staff_type = [
        [0, 'yes'],
        [1, 'no']
    ]
    member_type = [
        [0, 'yes'],
        [1, 'no']
    ]
    id = models.CharField(max_length=10, null=False, unique=True, blank=False, primary_key=True, verbose_name="会员号")
    register_date = models.DateField(null=False, blank=False, default=timezone.now, verbose_name='注册日')
    nickname = models.CharField(max_length=20, null=True, blank=True, verbose_name="昵称")
    gender = models.IntegerField(choices=gender_type, null=True, blank=True, verbose_name="性别")
    roles = models.IntegerField(choices=role_type, default=1, verbose_name="角色")
    is_member = models.IntegerField(choices=member_type, default=1, verbose_name="是否是会员")
    member_expire_date = models.DateTimeField(null=True, blank=True, verbose_name="会员有效期")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="出生日期")
    email = models.CharField(max_length=40, null=True, blank=True, verbose_name="Email")
    is_staff = models.IntegerField(choices=staff_type, default=1, verbose_name="员工")
    user_phone = models.CharField(
        max_length=11,  # 假设手机号长度为11位
        unique=True,
        null=False,
        verbose_name='手机号',
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message="手机号格式不正确"
            )
        ]
    )

    last_login = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="last login")

    USERNAME_FIELD = 'user_phone'

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        pass
