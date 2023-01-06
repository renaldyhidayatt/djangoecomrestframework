from django.contrib.auth.models import UserManager


class MyUserManager(UserManager):
    def create_user(
        self, username, email, first_name, last_name, password=None, **extra_fields
    ):
        """Create and save a new user"""
        if not username:
            raise ValueError("The username field must be set")

        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """Create and save a new superuser"""
        user = self.create_user(username, email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def get_admin(self):
        return UserManager.filter(self, is_superuser=True).first()
