import secrets
from django.db import models
from django.contrib.auth.models import User


class UserSecretKey(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    secret_key = models.CharField("Secret Key", max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="secret_key_created_by"
    )
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="campaign_modified_by",
        null=True,
        blank=True
    )
    private_key_host = models.TextField("private_key_host", blank=True, null=True, max_length=4596)
    public_key_host = models.TextField("public_key_host", blank=True, null=True, max_length=4596)
    public_key_partner = models.TextField("public_key_partner", blank=True, null=True, max_length=4596)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class UserToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    token = models.CharField("token", max_length=96, unique=True)
    expiration_datetime = models.BigIntegerField("expiration_epoch")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="token_created_by",
        null=True,
        blank=True
    )
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="token_modified_by",
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.token

    def __str__(self):
        return f"{self.user.username} {self.token}"

    class Meta(object):
        """ Meta : for user token."""
        ordering = ['-created_at']
        db_table = "user_token"
        verbose_name = "user_tokens"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['token'])
        ]

# class ServiceAuth(models.Model):
#     name = models.CharField( max_length=256, null=False, blank=False, unique=True )
#     description = models.CharField( max_length=512, null=True, blank=True )

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="user_auth_created_by",
#         db_column='created_by'
#     )

#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Modified By",
#         related_name="user_auth_modified_by",
#         db_column='modified_by',
#         null=True,
#         blank=True
#     )


#     created_at = models.DateTimeField("Created At", auto_now_add=True)
#     modified_at = models.DateTimeField("Modified At", auto_now=True, null=True)

#     def __str__(self):
#         return "{}".format(self.name)

#     class Meta(object):
#         """ Meta : for ServiceAuth metadata."""
#         ordering = ['-created_at',]
#         db_table = "service_auth"
#         verbose_name = "service_auth"
#         verbose_name_plural = "services_auth"
#         indexes = [
#             models.Index(fields=['name']),
#         ]


# class UserAuth(models.Model):
#     def random_id():
#         return secrets.token_hex(16)

#     email = models.EmailField( max_length=256, null=False, blank=False )
#     hash_secret = models.CharField( max_length=512, null=False, blank=False )
#     clientid = models.CharField( max_length=256, null=False, blank=False, unique=True )

#     private_key_host = models.TextField("private_key_host", blank=True, null=True, max_length=4596)
#     public_key_host = models.TextField("public_key_host", blank=True, null=True, max_length=4596)
#     public_key_partner = models.TextField("public_key_partner", blank=True, null=True, max_length=4596)


#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="user_auth_created_by",
#         db_column='created_by'
#     )

#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Modified By",
#         related_name="user_auth_modified_by",
#         db_column='modified_by',
#         null=True,
#         blank=True
#     )


#     created_at = models.DateTimeField("Created At", auto_now_add=True)
#     modified_at = models.DateTimeField("Modified At", auto_now=True, null=True)

#     def __str__(self):
#         return "{}".format(self.clientid)

#     class Meta(object):
#         """ Meta : for Users metadata."""
#         ordering = ['-created_at',]
#         db_table = "user_auth"
#         verbose_name = "user_auth"
#         verbose_name_plural = "users_auth"
#         indexes = [
#             models.Index(fields=['clientid']),
#         ]


# class GroupAuth(models.Model):
#     name = models.CharField( max_length=256, null=False, blank=False, unique=True )

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="user_auth_created_by",
#         db_column='created_by'
#     )

#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Modified By",
#         related_name="user_auth_modified_by",
#         db_column='modified_by',
#         null=True,
#         blank=True
#     )


#     created_at = models.DateTimeField("Created At", auto_now_add=True)
#     modified_at = models.DateTimeField("Modified At", auto_now=True, null=True)

#     def __str__(self):
#         return "{}".format(self.name)

#     class Meta(object):
#         """ Meta : for GroupAuth metadata."""
#         ordering = ['-created_at',]
#         db_table = "group_auth"
#         verbose_name = "group_auth"
#         verbose_name_plural = "groups_auth"
#         indexes = [
#             models.Index(fields=['name']),
#         ]


# class PermissionsAuth(models.Model):
#     name = models.CharField( max_length=256, null=False, blank=False, unique=True )

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="user_auth_created_by",
#         db_column='created_by'
#     )

#     serviceAuth = models.ForeignKey(
#         ServiceAuth ,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="service_auth_created_by",
#         db_column='service_auth'
#     )

#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Modified By",
#         related_name="user_auth_modified_by",
#         db_column='modified_by',
#         null=True,
#         blank=True
#     )


#     created_at = models.DateTimeField("Created At", auto_now_add=True)
#     modified_at = models.DateTimeField("Modified At", auto_now=True, null=True)

#     def __str__(self):
#         return "{}".format(self.name)

#     class Meta(object):
#         """ Meta : for PermissionAuth metadata."""
#         ordering = ['-created_at',]
#         db_table = "permission_auth"
#         verbose_name = "permission_auth"
#         verbose_name_plural = "permissions_auth"
#         indexes = [
#             models.Index(fields=['name']),
#         ]

# class UserGroup(models.Model):
#     userAuth = models.ForeignKey(
#         UserAuth,
#         on_delete=models.CASCADE,
#         verbose_name="user auth",
#         related_name="UserAuth_ID",
#         db_column='user_auth'
#     )

#     groupAuth = models.ForeignKey(
#         GroupAuth,
#         on_delete=models.CASCADE,
#         verbose_name="user_group auth",
#         related_name="user_group_auth_id",
#         db_column='group_auth'
#     )

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="user_auth_created_by",
#         db_column='created_by'
#     )

#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Modified By",
#         related_name="user_auth_modified_by",
#         db_column='modified_by',
#         null=True,
#         blank=True
#     )


#     created_at = models.DateTimeField("Created At", auto_now_add=True)
#     modified_at = models.DateTimeField("Modified At", auto_now=True, null=True)

#     def __str__(self):
#         return "{}".format(self.id)

#     class Meta(object):
#         """ Meta : for UsersGroup metadata."""
#         ordering = ['-created_at',]
#         db_table = "user_group"
#         verbose_name = "user_group"
#         verbose_name_plural = "users_group"

# class PermissionGroup(models.Model):
#     permissionAuth = models.ForeignKey(
#         PermissionsAuth,
#         on_delete=models.CASCADE,
#         verbose_name="permission group auth",
#         related_name="permission_group_id",
#         db_column='permission_auth'
#     )

#     groupAuth = models.ForeignKey(
#         GroupAuth,
#         on_delete=models.CASCADE,
#         verbose_name="group_permission auth",
#         related_name="group_permission_ID",
#         db_column='group_auth'
#     )

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Created By",
#         related_name="user_auth_created_by",
#         db_column='created_by'
#     )

#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Modified By",
#         related_name="user_auth_modified_by",
#         db_column='modified_by',
#         null=True,
#         blank=True
#     )


#     created_at = models.DateTimeField("Created At", auto_now_add=True)
#     modified_at = models.DateTimeField("Modified At", auto_now=True, null=True)

#     def __str__(self):
#         return "{}".format(self.id)

#     class Meta(object):
#         """ Meta : for PermissionGroup metadata."""
#         ordering = ['-created_at',]
#         db_table = "permission_group"
#         verbose_name = "permission_group"
#         verbose_name_plural = "permissions_group"
