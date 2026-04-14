#Creates player objects. Each object contains the number of a specific player and a boolean for imposter
class Player:
    #atributes: p_num, is_imposter


    def __init__(self, num, imposter):
        self.p_num = num
        self.is_imposter = imposter
        
        
    
    
    def get_info(self):
        return (self.p_num, self.is_imposter)
        
    def __str__(self):
        return f"({self.p_num}, {self.is_imposter})"
    
    def __repr__(self):
        return self.__str__()
