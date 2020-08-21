from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, 
    DateField, IntegerField,
    FloatField, SelectMultipleField
)
from wtforms.validators import DataRequired, URL, NumberRange

country_choices = [
    ('Afghanistan', 'Afghanistan'), 
    ('Albania', 'Albania'), 
    ('Algeria', 'Algeria'), 
    ('Andorra', 'Andorra'), 
    ('Angola', 'Angola'), 
    ('Antigua & Deps', 'Antigua & Deps'), 
    ('Argentina', 'Argentina'), 
    ('Armenia', 'Armenia'), 
    ('Australia', 'Australia'), 
    ('Austria', 'Austria'), 
    ('Azerbaijan', 'Azerbaijan'), 
    ('Bahamas', 'Bahamas'), 
    ('Bahrain', 'Bahrain'), 
    ('Bangladesh', 'Bangladesh'), 
    ('Barbados', 'Barbados'), 
    ('Belarus', 'Belarus'), 
    ('Belgium', 'Belgium'), 
    ('Belize', 'Belize'), 
    ('Benin', 'Benin'), 
    ('Bhutan', 'Bhutan'), 
    ('Bolivia', 'Bolivia'), 
    ('Bosnia Herzegovina', 'Bosnia Herzegovina'), 
    ('Botswana', 'Botswana'), 
    ('Brazil', 'Brazil'), 
    ('Brunei', 'Brunei'), 
    ('Bulgaria', 'Bulgaria'), 
    ('Burkina', 'Burkina'), 
    ('Burundi', 'Burundi'), 
    ('Cambodia', 'Cambodia'), 
    ('Cameroon', 'Cameroon'), 
    ('Canada', 'Canada'), 
    ('Cape Verde', 'Cape Verde'), 
    ('Central African Rep', 'Central African Rep'), 
    ('Chad', 'Chad'), 
    ('Chile', 'Chile'), 
    ('China', 'China'), 
    ('Colombia', 'Colombia'), 
    ('Comoros', 'Comoros'), 
    ('Congo', 'Congo'), 
    ('Costa Rica', 'Costa Rica'),
    ('Croatia', 'Croatia'), 
    ('Cuba', 'Cuba'), 
    ('Cyprus', 'Cyprus'), 
    ('Czech Republic', 'Czech Republic'), 
    ('Denmark', 'Denmark'), 
    ('Djibouti', 'Djibouti'), 
    ('Dominica', 'Dominica'), 
    ('Dominican Republic', 'Dominican Republic'), 
    ('East Timor', 'East Timor'), 
    ('Ecuador', 'Ecuador'), 
    ('Egypt', 'Egypt'), 
    ('El Salvador', 'El Salvador'), 
    ('Equatorial Guinea', 'Equatorial Guinea'), 
    ('Eritrea', 'Eritrea'), 
    ('Estonia', 'Estonia'), 
    ('Ethiopia', 'Ethiopia'), 
    ('Fiji', 'Fiji'), 
    ('Finland', 'Finland'), 
    ('France', 'France'), 
    ('Gabon', 'Gabon'), 
    ('Gambia', 'Gambia'), 
    ('Georgia', 'Georgia'), 
    ('Germany', 'Germany'), 
    ('Ghana', 'Ghana'), 
    ('Greece', 'Greece'), 
    ('Grenada', 'Grenada'), 
    ('Guatemala', 'Guatemala'), 
    ('Guinea', 'Guinea'), 
    ('Guinea-Bissau', 'Guinea-Bissau'), 
    ('Guyana', 'Guyana'), 
    ('Haiti', 'Haiti'), 
    ('Honduras', 'Honduras'), 
    ('Hungary', 'Hungary'), 
    ('Iceland', 'Iceland'), 
    ('India', 'India'), 
    ('Indonesia', 'Indonesia'), 
    ('Iran', 'Iran'), 
    ('Iraq', 'Iraq'), 
    ('Ireland', 'Ireland'), 
    ('Israel', 'Israel'), 
    ('Italy', 'Italy'), 
    ('Ivory Coast', 'Ivory Coast'), 
    ('Jamaica', 'Jamaica'), 
    ('Japan', 'Japan'), 
    ('Jordan', 'Jordan'), 
    ('Kazakhstan', 'Kazakhstan'), 
    ('Kenya', 'Kenya'), 
    ('Kiribati', 'Kiribati'), 
    ('Korea North', 'Korea North'), 
    ('Korea South', 'Korea South'), 
    ('Kosovo', 'Kosovo'), 
    ('Kuwait', 'Kuwait'), 
    ('Kyrgyzstan', 'Kyrgyzstan'), 
    ('Laos', 'Laos'), 
    ('Latvia', 'Latvia'), 
    ('Lebanon', 'Lebanon'), 
    ('Lesotho', 'Lesotho'), 
    ('Liberia', 'Liberia'), 
    ('Libya', 'Libya'), 
    ('Liechtenstein', 'Liechtenstein'), 
    ('Lithuania', 'Lithuania'), 
    ('Luxembourg', 'Luxembourg'), 
    ('Macedonia', 'Macedonia'), 
    ('Madagascar', 'Madagascar'), 
    ('Malawi', 'Malawi'), 
    ('Malaysia', 'Malaysia'), 
    ('Maldives', 'Maldives'), 
    ('Mali', 'Mali'), 
    ('Malta', 'Malta'), 
    ('Marshall Islands', 'Marshall Islands'), 
    ('Mauritania', 'Mauritania'), 
    ('Mauritius', 'Mauritius'), 
    ('Mexico', 'Mexico'), 
    ('Micronesia', 'Micronesia'), 
    ('Moldova', 'Moldova'), 
    ('Monaco', 'Monaco'), 
    ('Mongolia', 'Mongolia'), 
    ('Montenegro', 'Montenegro'), 
    ('Morocco', 'Morocco'), 
    ('Mozambique', 'Mozambique'), 
    ('Myanmar', 'Myanmar'), 
    ('Namibia', 'Namibia'), 
    ('Nauru', 'Nauru'), 
    ('Nepal', 'Nepal'), 
    ('Netherlands', 'Netherlands'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'), 
    ('Niger', 'Niger'), 
    ('Nigeria', 'Nigeria'), 
    ('Norway', 'Norway'), 
    ('Oman', 'Oman'), 
    ('Pakistan', 'Pakistan'), 
    ('Palau', 'Palau'), 
    ('Panama', 'Panama'), 
    ('Papua New Guinea', 'Papua New Guinea'), 
    ('Paraguay', 'Paraguay'), 
    ('Peru', 'Peru'), 
    ('Philippines', 'Philippines'), 
    ('Poland', 'Poland'), 
    ('Portugal', 'Portugal'), 
    ('Qatar', 'Qatar'), 
    ('Romania', 'Romania'), 
    ('Russian Federation', 'Russian Federation'), 
    ('Rwanda', 'Rwanda'), 
    ('St Kitts & Nevis', 'St Kitts & Nevis'), 
    ('St Lucia', 'St Lucia'), 
    ('Saint Vincent & the Grenadines', 'Saint Vincent & the Grenadines'), 
    ('Samoa', 'Samoa'), 
    ('San Marino', 'San Marino'), 
    ('Sao Tome & Principe', 'Sao Tome & Principe'), 
    ('Saudi Arabia', 'Saudi Arabia'), 
    ('Senegal', 'Senegal'), 
    ('Serbia', 'Serbia'), 
    ('Seychelles', 'Seychelles'), 
    ('Sierra Leone', 'Sierra Leone'), 
    ('Singapore', 'Singapore'), 
    ('Slovakia', 'Slovakia'), 
    ('Solomon Islands', 'Solomon Islands'), 
    ('Somalia', 'Somalia'), 
    ('South Africa', 'South Africa'), 
    ('South Sudan', 'South Sudan'),
    ('Spain', 'Spain'), 
    ('Sri Lanka', 'Sri Lanka'), 
    ('Sudan', 'Sudan'), 
    ('Suriname', 'Suriname'), 
    ('Swaziland', 'Swaziland'), 
    ('Sweden', 'Sweden'), 
    ('Switzerland', 'Switzerland'), 
    ('Syria', 'Syria'), 
    ('Tajikistan', 'Tajikistan'), 
    ('Tanzania', 'Tanzania'), 
    ('Thailand', 'Thailand'), 
    ('Togo', 'Togo'), 
    ('Tonga', 'Tonga'), 
    ('Trinidad & Tobago', 'Trinidad & Tobago'), 
    ('Tunisia', 'Tunisia'), 
    ('Turkey', 'Turkey'), 
    ('Turkmenistan', 'Turkmenistan'), 
    ('Tuvalu', 'Tuvalu'), 
    ('Uganda', 'Uganda'), 
    ('Ukraine', 'Ukraine'), 
    ('United Arab Emirates', 'United Arab Emirates'), 
    ('United Kingdom', 'United Kingdom'), 
    ('United States', 'United States'), 
    ('Uruguay', 'Uruguay'), 
    ('Uzbekistan', 'Uzbekistan'), 
    ('Vanuatu', 'Vanuatu'), 
    ('Vatican City', 'Vatican City'), 
    ('Venezuela', 'Venezuela'), 
    ('Vietnam', 'Vietnam'), 
    ('Yemen', 'Yemen'), 
    ('Zambia', 'Zambia'), 
    ('Zimbabwe', 'Zimbabwe')
]


nationality_choices = [
    ('Afghan', 'Afghan'), 
    ('Albanian', 'Albanian'), 
    ('Algerian', 'Algerian'), 
    ('American', 'American'), 
    ('Andorran', 'Andorran'), 
    ('Angolan', 'Angolan'), 
    ('Antiguans', 'Antiguans'), 
    ('Argentinean', 'Argentinean'), 
    ('Armenian', 'Armenian'), 
    ('Australian', 'Australian'), 
    ('Austrian', 'Austrian'), 
    ('Azerbaijani', 'Azerbaijani'), 
    ('Bahamian', 'Bahamian'), 
    ('Bahraini', 'Bahraini'), 
    ('Bangladeshi', 'Bangladeshi'), 
    ('Barbadian', 'Barbadian'), 
    ('Barbudans', 'Barbudans'), 
    ('Batswana', 'Batswana'), 
    ('Belarusian', 'Belarusian'), 
    ('Belgian', 'Belgian'), 
    ('Belizean', 'Belizean'), 
    ('Beninese', 'Beninese'), 
    ('Bhutanese', 'Bhutanese'), 
    ('Bolivian', 'Bolivian'), 
    ('Bosnian', 'Bosnian'), 
    ('Brazilian', 'Brazilian'), 
    ('British', 'British'), 
    ('Bruneian', 'Bruneian'), 
    ('Bulgarian', 'Bulgarian'), 
    ('Burkinabe', 'Burkinabe'), 
    ('Burmese', 'Burmese'), 
    ('Burundian', 'Burundian'), 
    ('Cambodian', 'Cambodian'), 
    ('Cameroonian', 'Cameroonian'), 
    ('Canadian', 'Canadian'), 
    ('Cape Verdean', 'Cape Verdean'), 
    ('Central African', 'Central African'), 
    ('Chadian', 'Chadian'), 
    ('Chilean', 'Chilean'), 
    ('Chinese', 'Chinese'), 
    ('Colombian', 'Colombian'), 
    ('Comoran', 'Comoran'), 
    ('Congolese', 'Congolese'), 
    ('Costa Rican', 'Costa Rican'), 
    ('Croatian', 'Croatian'), 
    ('Cuban', 'Cuban'), 
    ('Cypriot', 'Cypriot'), 
    ('Czech', 'Czech'), 
    ('Danish', 'Danish'), 
    ('Djibouti', 'Djibouti'), 
    ('Dominican', 'Dominican'), 
    ('Dutch', 'Dutch'), 
    ('East Timorese', 'East Timorese'), 
    ('Ecuadorean', 'Ecuadorean'), 
    ('Egyptian', 'Egyptian'), 
    ('Emirian', 'Emirian'), 
    ('Equatorial Guinean', 'Equatorial Guinean'), 
    ('Eritrean', 'Eritrean'), 
    ('Estonian', 'Estonian'), 
    ('Ethiopian', 'Ethiopian'), 
    ('Fijian', 'Fijian'), 
    ('Filipino', 'Filipino'), 
    ('Finnish', 'Finnish'), 
    ('French', 'French'), 
    ('Gabonese', 'Gabonese'), 
    ('Gambian', 'Gambian'), 
    ('Georgian', 'Georgian'), 
    ('German', 'German'), 
    ('Ghanaian', 'Ghanaian'), 
    ('Greek', 'Greek'), 
    ('Grenadian', 'Grenadian'), 
    ('Guatemalan', 'Guatemalan'), 
    ('Guinea-Bissauan', 'Guinea-Bissauan'), 
    ('Guinean', 'Guinean'), 
    ('Guyanese', 'Guyanese'), 
    ('Haitian', 'Haitian'), 
    ('Herzegovinian', 'Herzegovinian'), 
    ('Honduran', 'Honduran'), 
    ('Hungarian', 'Hungarian'), 
    ('Icelander', 'Icelander'), 
    ('Indian', 'Indian'), 
    ('Indonesian', 'Indonesian'), 
    ('Iranian', 'Iranian'), 
    ('Iraqi', 'Iraqi'), 
    ('Irish', 'Irish'), 
    ('Israeli', 'Israeli'), 
    ('Italian', 'Italian'), 
    ('Ivorian', 'Ivorian'), 
    ('Jamaican', 'Jamaican'), 
    ('Japanese', 'Japanese'), 
    ('Jordanian', 'Jordanian'), 
    ('Kazakhstani', 'Kazakhstani'), 
    ('Kenyan', 'Kenyan'), 
    ('Kittian & Nevisian', 'Kittian & Nevisian'), 
    ('Kuwaiti', 'Kuwaiti'), 
    ('Kyrgyz', 'Kyrgyz'), 
    ('Laotian', 'Laotian'), 
    ('Latvian', 'Latvian'), 
    ('Lebanese', 'Lebanese'), 
    ('Liberian', 'Liberian'), 
    ('Libyan', 'Libyan'), 
    ('Liechtensteiner', 'Liechtensteiner'), 
    ('Lithuanian', 'Lithuanian'), 
    ('Luxembourger', 'Luxembourger'), 
    ('Macedonian', 'Macedonian'), 
    ('Malagasy', 'Malagasy'), 
    ('Malawian', 'Malawian'), 
    ('Malaysian', 'Malaysian'), 
    ('Maldivan', 'Maldivan'), 
    ('Malian', 'Malian'), 
    ('Maltese', 'Maltese'), 
    ('Marshallese', 'Marshallese'), 
    ('Mauritanian', 'Mauritanian'), 
    ('Mauritian', 'Mauritian'), 
    ('Mexican', 'Mexican'), 
    ('Micronesian', 'Micronesian'), 
    ('Moldovan', 'Moldovan'), 
    ('Monacan', 'Monacan'), 
    ('Mongolian', 'Mongolian'), 
    ('Moroccan', 'Moroccan'), 
    ('Mosotho', 'Mosotho'), 
    ('Motswana', 'Motswana'), 
    ('Mozambican', 'Mozambican'), 
    ('Namibian', 'Namibian'), 
    ('Nauruan', 'Nauruan'), 
    ('Nepalese', 'Nepalese'), 
    ('New Zealander', 'New Zealander'), 
    ('Ni-Vanuatu', 'Ni-Vanuatu'), 
    ('Nicaraguan', 'Nicaraguan'), 
    ('Nigerien', 'Nigerien'), 
    ('North Korean', 'North Korean'), 
    ('Northern Irish', 'Northern Irish'), 
    ('Norwegian', 'Norwegian'), 
    ('Omani', 'Omani'), 
    ('Pakistani', 'Pakistani'), 
    ('Palauan', 'Palauan'), 
    ('Panamanian', 'Panamanian'), 
    ('Papua New Guinean', 'Papua New Guinean'), 
    ('Paraguayan', 'Paraguayan'), 
    ('Peruvian', 'Peruvian'), 
    ('Polish', 'Polish'), 
    ('Portuguese', 'Portuguese'), 
    ('Qatari', 'Qatari'), 
    ('Romanian', 'Romanian'), 
    ('Russian', 'Russian'), 
    ('Rwandan', 'Rwandan'), 
    ('Saint Lucian', 'Saint Lucian'),
    ('Salvadoran', 'Salvadoran'), 
    ('Samoan', 'Samoan'), 
    ('San Marinese', 'San Marinese'), 
    ('Sao Tomean', 'Sao Tomean'), 
    ('Saudi', 'Saudi'), 
    ('Scottish', 'Scottish'), 
    ('Senegalese', 'Senegalese'), 
    ('Serbian', 'Serbian'), 
    ('Seychellois', 'Seychellois'), 
    ('Sierra Leonean', 'Sierra Leonean'), 
    ('Singaporean', 'Singaporean'), 
    ('Slovakian', 'Slovakian'), 
    ('Slovenian', 'Slovenian'), 
    ('Solomon Islander', 'Solomon Islander'), 
    ('Somali', 'Somali'), 
    ('South African', 'South African'), 
    ('South Korean', 'South Korean'), 
    ('Spanish', 'Spanish'), 
    ('Sri Lankan', 'Sri Lankan'), 
    ('Sudanese', 'Sudanese'), 
    ('Surinamer', 'Surinamer'), 
    ('Swazi', 'Swazi'), 
    ('Swedish', 'Swedish'), 
    ('Swiss', 'Swiss'), 
    ('Syrian', 'Syrian'), 
    ('Taiwanese', 'Taiwanese'), 
    ('Tajik', 'Tajik'), 
    ('Tanzanian', 'Tanzanian'), 
    ('Thai', 'Thai'), 
    ('Togolese', 'Togolese'), 
    ('Tongan', 'Tongan'), 
    ('Trinidadian / Tobagonian', 'Trinidadian / Tobagonian'), 
    ('Tunisian', 'Tunisian'), 
    ('Turkish', 'Turkish'), 
    ('Tuvaluan', 'Tuvaluan'), 
    ('Ugandan', 'Ugandan'), 
    ('Ukrainian', 'Ukrainian'), 
    ('Uruguayan', 'Uruguayan'), 
    ('Uzbekistani', 'Uzbekistani'), 
    ('Venezuelan', 'Venezuelan'), 
    ('Vietnamese', 'Vietnamese'), 
    ('Welsh', 'Welsh'), 
    ('Yemenite', 'Yemenite'), 
    ('Zambian', 'Zambian'), 
    ('Zimbabwean', 'Zimbabwean')
]


awards_choices = [
    ("Aga Khan Award for Architecture", "Aga Khan Award for Architecture"), 
    ("Africa Architecture Awards", "Africa Architecture Awards"), 
    ("AIA Gold Medal", "AIA Gold Medal"),
    ("Alvar Aalto Medal", "Alvar Aalto Medal"),
    ("Erich Schelling Architecture Award", "Erich Schelling Architecture Award"),  
    ("Erich Schelling Architecture Theory Award", "Erich Schelling Architecture Theory Award"),
    ("EU Mies Award", "EU Mies Award"), 
    ("Global Award for Sustainable Architecture", "Global Award for Sustainable Architecture"), 
    ("Good Design Award", "Good Design Award"),  
    ("Green Good Design", "Green Good Design"), 
    ("International Architecture Awards", "International Architecture Awards"), 
    ("Jane Drew Prize", "Jane Drew Prize"), 
    ("Louis I. Kahn Memorial Award", "Louis I. Kahn Memorial Award"), 
    ("Praemium Imperiale", "Praemium Imperiale"), 
    ("Pritzker Prize", "Pritzker Prize"), 
    ("RAIC International Prize", "RAIC International Prize"), 
    ("RIBA Annie Spink Award", "RIBA Annie Spink Award"), 
    ("RIBA President's Medals", "RIBA President's Medals"), 
    ("Royal Gold Medal", "Royal Gold Medal"), 
    ("Swiss Architectural Award", "Swiss Architectural Award"), 
    ("Thomas Jefferson Medal in Architecture", "Thomas Jefferson Medal in Architecture"), 
    ("International Highrise Award", "International Highrise Award"), 
    ("UIA Gold Medal", "UIA Gold Medal"),
    ("Venice Biennale of Architecture", "Venice Biennale of Architecture"), 
    ("Wolf Prize in Arts", "Wolf Prize in Arts"), 
    ("World Architecture Festival", "World Architecture Festival") 
]

transports_choices = [
    ('boat', 'boat'),
    ('cable_car', 'cable_car'),
    ('bike', 'bike'),
    ('bus', 'bus'),
    ('helicopter','helicopter'),
    ('light_rail', 'light_rail'),
    ('metro', 'metro'),
    ('taxi', 'taxi'),
    ('train', 'train'),
    ('tram', 'tram')
]



class ArchitectureForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    completed_year = IntegerField(
        'completed_year', validators=[NumberRange(min=0, max=2100)]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    latitude = FloatField(
        'latitude', validators=[NumberRange(min=-90, max=90)]
    )
    longitude = FloatField(
        'longitude', validators=[NumberRange(min=-180, max=180)]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    architect_id = StringField(
        'architect_id', validators=[DataRequired()]
    )
    city_id = StringField(
        'city_id', validators=[DataRequired()]
    )
    has_more_info = SelectField(
        'has_more_info',
        choices=[
            ('No', 'No'),            
            ('Yes', 'Yes')
        ]
    )
    info = StringField(
        'info'
    )
    other_image_link_1 = StringField(
        'other_image_link_1'
    )
    other_image_link_2 = StringField(
        'other_image_link_2'
    )
    other_image_link_3 = StringField(
        'other_image_link_3'
    )


class CityForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    country = SelectField(
        'country', validators=[DataRequired()],
        choices = country_choices
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    transports = SelectMultipleField(
        'transports', 
        choices = transports_choices
    )
    has_more_info = SelectField(
        'has_more_info',
        choices=[
            ('No', 'No'),            
            ('Yes', 'Yes')
        ]
    )
    info = StringField(
        'info'
    )


class ArchitectForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices = [
            ('Male', 'Male'), 
            ('Female', 'Female')
        ]
    )
    birthday = DateField(
        'birthday', validators=[DataRequired()]
    )
    birthplace = StringField(
        'birthplace', validators=[DataRequired()]
    )
    nationality = SelectField(
        'nationality', validators=[DataRequired()],
        choices = nationality_choices
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    has_quote = SelectField(
        'has_quote',
        choices=[
            ('No', 'No'),            
            ('Yes', 'Yes')
        ]
    )
    quote = StringField(
        'quote'
    )
    awards = SelectMultipleField(
        'awards', 
        choices = awards_choices
    )

