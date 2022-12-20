from rest_framework import serializers
from account.models import User, MenuGroup, MenuMaster, TaskMaster, UserTaskAccess, FieldMaster, TaskFieldMaster
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from account.utils import Util
import socket

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email','usr','username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']
    def validate(self,attrs):
        user= self.context.get('user')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordChangeEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('encoded id:',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Pass reset Token:',token)
            link = 'http://localhost:8000/account/api/reset/'+uid+'/'+token
            print('link;',link)
            body='Click Following Link to Reset your Password ' +link
            data={
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email

            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr('You are not Registered.')
        # return super().validate(attrs)

class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']
    def validate(self,attrs):
        try:
            uid= self.context.get('uid')
            token= self.context.get('token')

            password = attrs.get('password')
            password2 = attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password does not match')
            id = smart_str(urlsafe_base64_decode(uid))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not valid or expired.')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is expired or invalid')

class MenuGrpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuGroup
        fields =['id', 'grpname', 'sequence', 'inactive', 'note']

class MenuMasterserializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMaster
        fields = ['id', 'groupname', 'menuname', 'taskname']



lastupdateipser = socket.gethostbyname(socket.gethostname())

class TaskMasterSerializer(serializers.ModelSerializer):    
           
    # lastupdateip=serializers.CharField(source=lastupdateipser)
    # lastupdateip = socket.gethostbyname(socket.gethostname())
    # print(lastupdateip)
    # lastupdateip = serializers.IPAddressField()
    # lastupdateip = lastip
    class Meta:
        model = TaskMaster
        fields = ['id', 'task', 'description', 'pyname', 'inactivetask', 'notetask', 'lastupdateuser', 'lastupdatetask','lastupdateip' ]
 

lastupdateipser = socket.gethostbyname(socket.gethostname())
class UserTaskAccessSerializer(serializers.ModelSerializer):
    
    lastupdateip=serializers.CharField(source=lastupdateipser)
    class Meta:
        model = UserTaskAccess
        fields = [ 'id','taskuseracc','taskacc','pynameacc','inactivetaskacc','notetaskacc','viewaccess','addaccess','editaccess','deleteaccess',
    'inactiveaccess','lastupdateuseracc','lastupdatetaskacc'] 

class FieldMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldMaster
        fields = ['id','fieldmas','placeholdermsg','errormsg','inactivefield','notefield','lastupdateuserfield',
        'lastupdatedatefield','lastupdatetimefield','lastupdatetaskfield','lastupdateipfield']

class TaskFieldMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFieldMaster
        fields = ['id','usertaskfield','tasktaskfield','fieldtaskfield','restricted','inactivetaskfield','notetaskfield',
        'lastupdateusertaskfield','lastupdatedatetaskfield','lastupdatetimetaskfield','lastupdatetasktaskfield','lastupdateiptaskfield']
