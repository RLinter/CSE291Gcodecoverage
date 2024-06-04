# https://medium.com/@tentotheminus9/python-oop-a-simple-diagnostic-test-example-b58b026951bd
class Patient():
    """
    Description:
        A parent class for the disease classess
    
    Attributes:
        first_name: First name
        last_name: Last name
        nhs_number: Unique NHS number
        age: Age
        sex: Sex
        region: Region most relevant to the patient
        
    Methods:
        NA
    """
    
    def __init__ (self, nhs_number, first_name, last_name, age, sex, region):
        self.nhs_number = nhs_number
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.region = region



from abc import ABC, abstractmethod

class Condition(object):
    """
    Description:
        An abstract parent class for the condition class
    
    Attributes:
        id: string
        name:string
        heart_rate_bpm: Heart rate in beats per minute
        pretest: float

    Methods:
        get_pretest: Get a probability from a database (hardcoded for now)
        generate_pretest: Calculate a probability from a set of symptoms
        enter_pretest: Allow the user to enter a probability
    
    """
    
    def __init__(self, id, name, heart_rate_bpm, pretest = 0):
        self.id = id
        self.name = name
        self.heart_rate_bpm = heart_rate_bpm
        self.pretest = pretest

    def get_pretest(self, disease):
            #SQL code here to access the medical database, using the 
            #'disease' key.
            #Imagine that we send and recieve back a value relevant to; 
            #id = covid19, Patient.region = Leeds, 
            #Patient.age = 55, Patient.sex = M
            pretest = 0.12
            return(pretest)

    @abstractmethod
    def generate_pretest(self):
        pass

    def enter_pretest(self, pretest_entered):
        self.pretest = pretest_entered


class Respiratory(Condition):
    """
    Description:
        An abstract class for the respiratory class
    
    Attributes:
        blood_oxygen_level: float
        temperature: float
        smoker: boolean
        sneezing: boolean
        runny_nose: boolean
        sore_throat: boolean
        headaches: boolean
        muscle_aches: boolean
        breathlessness: boolean

     Methods:
        NA
    """
    
    def __init__(self, blood_oxygen_level, temperature, smoker, sneezing, runny_nose, sore_throat,
                 headaches, muscle_aches, breathlessness):
                     
        #Condition.__init__(self, id, name, heart_rate_bpm, pretest)
                     
        self.blood_oxygen_level = blood_oxygen_level
        self.temperature = temperature
        self.smoker = smoker
        self.sneezing = sneezing
        self.runny_nose = runny_nose
        self.sore_throat = sore_throat
        self.headaches = headaches
        self.muscle_aches = muscle_aches
        self.breathlessness = breathlessness


class Covid19(Respiratory):
    """
    Description:
        A class for the Covid19 class
    
    Attributes:
        continuous_cough: Does the patient have a continuous cough?
        covid_proximity: Has the patient been near to someone else with confirmed Covid19?
        taste_change: Has the patient's taste changed recently?
        vaccinated: Has the patient been vaccinated in the last 12 months?

     Methods:
        get_pretest: Get the pretest based upon suspected condition ID, region, age, and sex
        generate_pretest: Get the pretest based upon symptoms
        enter_pretest: Enter the pretest based upon experience
    """
    
    def __init__(self, continuous_cough=None, covid_proximity=None, taste_change=None, vaccinated=None):
        
        #Respiratory.__init__(self, name, heart_rate_bpm, blood_oxygen_level, temperature, smoker, sneezing, runny_nose, 
         #                    sore_throat, headaches, muscle_aches, breathlessness)
                     
        self.continuous_cough = continuous_cough
        self.covid_proximity = covid_proximity
        self.taste_change = taste_change
        self.vaccinated = vaccinated
           
    def generate_pretest(self):
        score = 0
        if self.heart_rate_bpm > 100:
            score += 1
        if self.blood_oxygen_level <0.92:
            score += 1
        if self.temperature > 39:
            score += 1
        if self.smoker:
            score += 1
        if self.sneezing:
            score += 1
        if self.runny_nose:
            score += 1
        if self.sore_throat:
            score += 1
        if self.headaches:
            score += 1
        if self.muscle_aches:
            score += 1
        if self.breathlessness:
            score += 1
        if self.continuous_cough:
            score += 1
        if self.covid_proximity:
            score += 1
        if self.taste_change:
            score += 1
        if self.vaccinated:
            score -= 5
            
        pretest = score / 14
        if pretest < 0:
            pretest = 0
        
        pretest = round(pretest, 2)
        return(pretest)
    

class Test():
    """
    Description:
    
    Attributes:
        sensitivty: The test sensitivity, 0.0 - 1.0 (float)
        specificity: The test specificity, 0.0 - 1.0 (float)
        sensitivity_ci_upper: The upper 95% sensitvity confidence interval value
        sensitivity_ci_lower: The lower 95% sensitvity confidence interval value
        specificity_ci_upper: The upper 95% specificity confidence interval value
        specificity_ci_lower: The lower 95% specificity confidence interval value
        pretest: The pre-test (or 'prior') probability of disease (float)
        result: The result of the diagnostic test. Either positive or negative (string)

    Methods:
        __generate_posttest_general: Calculate post-test values (private)
        generate_posttest: Calculate post-test values using the above method, for the quoted, upper and lower values
    """

    def __init__(self, sensitivity, specificity, 
                  sensitivity_ci_upper, sensitivity_ci_lower, specificity_ci_upper,
                  specificity_ci_lower, pretest, result):
        
        """Initialise attributes"""
        self.sensitivity = sensitivity
        self.specificity = specificity
        self.sensitivity_ci_upper = sensitivity_ci_upper
        self.sensitivity_ci_lower = sensitivity_ci_lower
        self.specificity_ci_upper = specificity_ci_upper
        self.specificity_ci_lower = specificity_ci_lower
        self.pretest = pretest
        self.result = result
        
    def __generate_posttest_general(self, sensitivity_option, specificity_option, pretest, result):
        
        """Generate a post-test probability"""  
        lr_pos = sensitivity_option / (1 - specificity_option) 
        lr_neg = (1 - sensitivity_option) / specificity_option
        
        pre_odds = pretest / (1-pretest)
        post_odds_pos = pre_odds * lr_pos 
        post_odds_neg = pre_odds * lr_neg 
        post_pos = post_odds_pos / (1+post_odds_pos)
        post_neg = post_odds_neg / (1+post_odds_neg)
        
        if result == 'pos':
            return(round(post_pos, 3))
        
        if result == 'neg':
            return(round(post_neg, 3))
               
   
    def generate_posttest(self):

        #Generate results for each sens/spec level, given a pos or neg result,
        posttest_quoted = self.__generate_posttest_general(self.sensitivity, self.specificity, self.pretest, self.result)
        posttest_lower = self.__generate_posttest_general(self.sensitivity_ci_lower, self.specificity_ci_lower, self.pretest, self.result)
        posttest_upper = self.__generate_posttest_general(self.sensitivity_ci_upper, self.specificity_ci_upper, self.pretest, self.result)
                
        posttest_all = [posttest_quoted, posttest_lower, posttest_upper]
        
        return(posttest_all)
    














# patient1 = Covid19()
# pretest = patient1.get_pretest('covid19')

# test_for_covid19 = Test(sensitivity = 0.92, 
#                         specificity = 0.90, 
#                         sensitivity_ci_upper = 0.94, 
#                         sensitivity_ci_lower = 0.90, 
#                         specificity_ci_upper = 0.91, 
#                         specificity_ci_lower = 0.89, 
#                         pretest = pretest, 
#                         result = 'pos')

# posttest = test_for_covid19.generate_posttest()

# print("Based upon the test result, with a pre-test probability of " + 
# str(pretest) + ', the post-test probability is ' + str(posttest[0]) + ' (' + 
# str(posttest[1]) + '-' + str(posttest[2]) + ' 95% CI)')



# patient2 = Covid19()

# patient2.continuous_cough = False
# patient2.covid_proximity = False
# patient2.taste_change = False
# patient2.vaccinated = False
# patient2.heart_rate_bpm = 80
# patient2.blood_oxygen_level = 0.85
# patient2.temperature = 40
# patient2.smoker = True
# patient2.sneezing = False
# patient2.runny_nose = False
# patient2.sore_throat = False
# patient2.headaches = False
# patient2.muscle_aches = False
# patient2.breathlessness = True

# pretest = patient2.generate_pretest()

# test_for_covid19 = Test(sensitivity = 0.95, 
#                         specificity = 0.95, 
#                         sensitivity_ci_upper = 0.97, 
#                         sensitivity_ci_lower = 0.94, 
#                         specificity_ci_upper = 0.96, 
#                         specificity_ci_lower = 0.94, 
#                         pretest = pretest, 
#                         result = 'neg')

# posttest = test_for_covid19.generate_posttest()

# print("Based upon the test result, with a pre-test probability of " + str(pretest) + ', the post-test probability is ' + str(posttest[0]) + ' (' + str(posttest[2]) + '-' + str(posttest[1]) + ' 95% CI)')







# patient3 = Covid19()

# patient3.continuous_cough = True
# patient3.covid_proximity = True
# patient3.taste_change = True
# patient3.vaccinated = False
# patient3.heart_rate_bpm = 105
# patient3.blood_oxygen_level = 0.85
# patient3.temperature = 40
# patient3.smoker = True
# patient3.sneezing = False
# patient3.runny_nose = False
# patient3.sore_throat = False
# patient3.headaches = True
# patient3.muscle_aches = True
# patient3.breathlessness = True

# pretest = patient3.generate_pretest()

# test_for_covid19 = Test(sensitivity = 0.95, 
#                         specificity = 0.95, 
#                         sensitivity_ci_upper = 0.97, 
#                         sensitivity_ci_lower = 0.94, 
#                         specificity_ci_upper = 0.96, 
#                         specificity_ci_lower = 0.94, 
#                         pretest = pretest, 
#                         result = 'pos')

# posttest = test_for_covid19.generate_posttest()

# print("Based upon the test result, with a pre-test probability of " + str(pretest) + ', the post-test probability is ' + str(posttest[0]) + ' (' + str(posttest[1]) + '-' + str(posttest[2]) + ' 95% CI)')

