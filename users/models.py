from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


def humanize_date(date=None):
    date = datetime.date(date)
    now = datetime.date(datetime.now())
    if date:
        dt = date - now
        offset = dt.seconds + (dt.days * 60*60*24)
        delta_s = offset % 60
        offset /= 60
        delta_m = offset % 60
        offset /= 60
        delta_h = offset % 24
        offset /= 24
        delta_d = offset
    else:
        raise ValueError("Must supply a date (from now)")

    if delta_d > 1:
        if delta_d > 6:
            date = now + \
                datetime.timedelta(days=-delta_d, hours=-
                                   delta_h, minutes=-delta_m)
            return date.strftime('%A, %Y %B %m, %H:%I')
        else:
            wday = now + datetime.timedelta(days=-delta_d)
            return wday.strftime('%A')
    if delta_d == 1:
        return "Yesterday"
    if delta_h > 0:
        return "%dh%dm ago" % (delta_h, delta_m)
    if delta_m > 0:
        return "%dm%ds ago" % (delta_m, delta_s)
    else:
        return "%ds ago" % delta_s


COUNTRIES = (
    ('AD', ('Andorra')),
    ('AE', ('United Arab Emirates')),
    ('AF', ('Afghanistan')),
    ('AG', ('Antigua & Barbuda')),
    ('AI', ('Anguilla')),
    ('AL', ('Albania')),
    ('AM', ('Armenia')),
    ('AN', ('Netherlands Antilles')),
    ('AO', ('Angola')),
    ('AQ', ('Antarctica')),
    ('AR', ('Argentina')),
    ('AS', ('American Samoa')),
    ('AT', ('Austria')),
    ('AU', ('Australia')),
    ('AW', ('Aruba')),
    ('AZ', ('Azerbaijan')),
    ('BA', ('Bosnia and Herzegovina')),
    ('BB', ('Barbados')),
    ('BD', ('Bangladesh')),
    ('BE', ('Belgium')),
    ('BF', ('Burkina Faso')),
    ('BG', ('Bulgaria')),
    ('BH', ('Bahrain')),
    ('BI', ('Burundi')),
    ('BJ', ('Benin')),
    ('BM', ('Bermuda')),
    ('BN', ('Brunei Darussalam')),
    ('BO', ('Bolivia')),
    ('BR', ('Brazil')),
    ('BS', ('Bahama')),
    ('BT', ('Bhutan')),
    ('BV', ('Bouvet Island')),
    ('BW', ('Botswana')),
    ('BY', ('Belarus')),
    ('BZ', ('Belize')),
    ('CA', ('Canada')),
    ('CC', ('Cocos (Keeling) Islands')),
    ('CF', ('Central African Republic')),
    ('CG', ('Congo')),
    ('CH', ('Switzerland')),
    ('CI', ('Ivory Coast')),
    ('CK', ('Cook Iislands')),
    ('CL', ('Chile')),
    ('CM', ('Cameroon')),
    ('CN', ('China')),
    ('CO', ('Colombia')),
    ('CR', ('Costa Rica')),
    ('CU', ('Cuba')),
    ('CV', ('Cape Verde')),
    ('CX', ('Christmas Island')),
    ('CY', ('Cyprus')),
    ('CZ', ('Czech Republic')),
    ('DE', ('Germany')),
    ('DJ', ('Djibouti')),
    ('DK', ('Denmark')),
    ('DM', ('Dominica')),
    ('DO', ('Dominican Republic')),
    ('DZ', ('Algeria')),
    ('EC', ('Ecuador')),
    ('EE', ('Estonia')),
    ('EG', ('Egypt')),
    ('EH', ('Western Sahara')),
    ('ER', ('Eritrea')),
    ('ES', ('Spain')),
    ('ET', ('Ethiopia')),
    ('FI', ('Finland')),
    ('FJ', ('Fiji')),
    ('FK', ('Falkland Islands (Malvinas)')),
    ('FM', ('Micronesia')),
    ('FO', ('Faroe Islands')),
    ('FR', ('France')),
    ('FX', ('France, Metropolitan')),
    ('GA', ('Gabon')),
    ('GB', ('United Kingdom (Great Britain)')),
    ('GD', ('Grenada')),
    ('GE', ('Georgia')),
    ('GF', ('French Guiana')),
    ('GH', ('Ghana')),
    ('GI', ('Gibraltar')),
    ('GL', ('Greenland')),
    ('GM', ('Gambia')),
    ('GN', ('Guinea')),
    ('GP', ('Guadeloupe')),
    ('GQ', ('Equatorial Guinea')),
    ('GR', ('Greece')),
    ('GS', ('South Georgia and the South Sandwich Islands')),
    ('GT', ('Guatemala')),
    ('GU', ('Guam')),
    ('GW', ('Guinea-Bissau')),
    ('GY', ('Guyana')),
    ('HK', ('Hong Kong')),
    ('HM', ('Heard & McDonald Islands')),
    ('HN', ('Honduras')),
    ('HR', ('Croatia')),
    ('HT', ('Haiti')),
    ('HU', ('Hungary')),
    ('ID', ('Indonesia')),
    ('IE', ('Ireland')),
    ('IL', ('Israel')),
    ('IN', ('India')),
    ('IO', ('British Indian Ocean Territory')),
    ('IQ', ('Iraq')),
    ('IR', ('Islamic Republic of Iran')),
    ('IS', ('Iceland')),
    ('IT', ('Italy')),
    ('JM', ('Jamaica')),
    ('JO', ('Jordan')),
    ('JP', ('Japan')),
    ('KE', ('Kenya')),
    ('KG', ('Kyrgyzstan')),
    ('KH', ('Cambodia')),
    ('KI', ('Kiribati')),
    ('KM', ('Comoros')),
    ('KN', ('St. Kitts and Nevis')),
    ('KP', ('Korea, Democratic People\'s Republic of')),
    ('KR', ('Korea, Republic of')),
    ('KW', ('Kuwait')),
    ('KY', ('Cayman Islands')),
    ('KZ', ('Kazakhstan')),
    ('LA', ('Lao People\'s Democratic Republic')),
    ('LB', ('Lebanon')),
    ('LC', ('Saint Lucia')),
    ('LI', ('Liechtenstein')),
    ('LK', ('Sri Lanka')),
    ('LR', ('Liberia')),
    ('LS', ('Lesotho')),
    ('LT', ('Lithuania')),
    ('LU', ('Luxembourg')),
    ('LV', ('Latvia')),
    ('LY', ('Libyan Arab Jamahiriya')),
    ('MA', ('Morocco')),
    ('MC', ('Monaco')),
    ('MD', ('Moldova, Republic of')),
    ('MG', ('Madagascar')),
    ('MH', ('Marshall Islands')),
    ('ML', ('Mali')),
    ('MN', ('Mongolia')),
    ('MM', ('Myanmar')),
    ('MO', ('Macau')),
    ('MP', ('Northern Mariana Islands')),
    ('MQ', ('Martinique')),
    ('MR', ('Mauritania')),
    ('MS', ('Monserrat')),
    ('MT', ('Malta')),
    ('MU', ('Mauritius')),
    ('MV', ('Maldives')),
    ('MW', ('Malawi')),
    ('MX', ('Mexico')),
    ('MY', ('Malaysia')),
    ('MZ', ('Mozambique')),
    ('NA', ('Namibia')),
    ('NC', ('New Caledonia')),
    ('NE', ('Niger')),
    ('NF', ('Norfolk Island')),
    ('NG', ('Nigeria')),
    ('NI', ('Nicaragua')),
    ('NL', ('Netherlands')),
    ('NO', ('Norway')),
    ('NP', ('Nepal')),
    ('NR', ('Nauru')),
    ('NU', ('Niue')),
    ('NZ', ('New Zealand')),
    ('OM', ('Oman')),
    ('PA', ('Panama')),
    ('PE', ('Peru')),
    ('PF', ('French Polynesia')),
    ('PG', ('Papua New Guinea')),
    ('PH', ('Philippines')),
    ('PK', ('Pakistan')),
    ('PL', ('Poland')),
    ('PM', ('St. Pierre & Miquelon')),
    ('PN', ('Pitcairn')),
    ('PR', ('Puerto Rico')),
    ('PT', ('Portugal')),
    ('PW', ('Palau')),
    ('PY', ('Paraguay')),
    ('QA', ('Qatar')),
    ('RE', ('Reunion')),
    ('RO', ('Romania')),
    ('RU', ('Russian Federation')),
    ('RW', ('Rwanda')),
    ('SA', ('Saudi Arabia')),
    ('SB', ('Solomon Islands')),
    ('SC', ('Seychelles')),
    ('SD', ('Sudan')),
    ('SE', ('Sweden')),
    ('SG', ('Singapore')),
    ('SH', ('St. Helena')),
    ('SI', ('Slovenia')),
    ('SJ', ('Svalbard & Jan Mayen Islands')),
    ('SK', ('Slovakia')),
    ('SL', ('Sierra Leone')),
    ('SM', ('San Marino')),
    ('SN', ('Senegal')),
    ('SO', ('Somalia')),
    ('SR', ('Suriname')),
    ('ST', ('Sao Tome & Principe')),
    ('SV', ('El Salvador')),
    ('SY', ('Syrian Arab Republic')),
    ('SZ', ('Swaziland')),
    ('TC', ('Turks & Caicos Islands')),
    ('TD', ('Chad')),
    ('TF', ('French Southern Territories')),
    ('TG', ('Togo')),
    ('TH', ('Thailand')),
    ('TJ', ('Tajikistan')),
    ('TK', ('Tokelau')),
    ('TM', ('Turkmenistan')),
    ('TN', ('Tunisia')),
    ('TO', ('Tonga')),
    ('TP', ('East Timor')),
    ('TR', ('Turkey')),
    ('TT', ('Trinidad & Tobago')),
    ('TV', ('Tuvalu')),
    ('TW', ('Taiwan, Province of China')),
    ('TZ', ('Tanzania, United Republic of')),
    ('UA', ('Ukraine')),
    ('UG', ('Uganda')),
    ('UM', ('United States Minor Outlying Islands')),
    ('US', ('United States of America')),
    ('UY', ('Uruguay')),
    ('UZ', ('Uzbekistan')),
    ('VA', ('Vatican City State (Holy See)')),
    ('VC', ('St. Vincent & the Grenadines')),
    ('VE', ('Venezuela')),
    ('VG', ('British Virgin Islands')),
    ('VI', ('United States Virgin Islands')),
    ('VN', ('Viet Nam')),
    ('VU', ('Vanuatu')),
    ('WF', ('Wallis & Futuna Islands')),
    ('WS', ('Samoa')),
    ('YE', ('Yemen')),
    ('YT', ('Mayotte')),
    ('YU', ('Yugoslavia')),
    ('ZA', ('South Africa')),
    ('ZM', ('Zambia')),
    ('ZR', ('Zaire')),
    ('ZW', ('Zimbabwe')),
    ('ZZ', ('Unknown or unspecified country')),
)


class Category(models.Model):
    title = models.CharField(max_length=50)
    is_muted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    # * Main
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(null=True, blank=True, max_length=20)
    is_confirmed = models.BooleanField(default=False)

    # Extra info
    about = models.CharField(
        max_length=190, default="Hi, I use Orgachat!", blank=True, null=True)
    avatar = models.FileField(
        upload_to='users/avatars', default="users/img/avatar/DefUser.png")
    country = models.CharField(choices=COUNTRIES, max_length=50, default="ZZ")

    # Society
    friends = models.ManyToManyField('User', blank=True)
    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)

    # advance for stuff
    email_code = models.IntegerField(blank=True, null=True)
    expo_push_token = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def to_json(self):
        try:
            categories = self.categories.all()
        except:
            categories = []
        return {
            "id": self.id,
            "username": self.username,
            "about": self.about,
            "avatar": self.avatar.url,
            "country": self.country,
            "categories": categories,
            'last_seen': humanize_date(self.last_seen),
        }

    def __str__(self):
        return str(self.username)
