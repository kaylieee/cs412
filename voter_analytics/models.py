from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Encapsulate the data of a Profile
    '''

    #define attributes
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    zip_code = models.IntegerField()
    apartment_number = models.TextField()
    dob = models.DateField()
    registration_date = models.DateField()
    party = models.CharField(max_length=2)
    precinct = models.CharField(max_length=2)
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.first_name} {self.last_name}: {self.party}, {self.precinct}'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    filename = '/Users/kaylie/Desktop/django/newton_voters.csv'
    f = open(filename, 'r')
    f.readline() 

    for line in f:
        fields = line.split(',')

        voter = Voter(last_name = fields[1],
                    first_name = fields[2],
                    street_number = fields[3],
                    street_name = fields[4],
                    zip_code = fields[6],
                    apartment_number = fields[5],
                    dob = fields[7],
                    registration_date = fields[8],
                    party = fields[9],
                    precinct = fields[10],
                    v20state = fields[11],
                    v21town = fields[12],
                    v21primary = fields[13],
                    v22general = fields[14],
                    v23town = fields[15],
                    voter_score = fields[16])
        print(f'Created voter: {voter}')
        voter.save()