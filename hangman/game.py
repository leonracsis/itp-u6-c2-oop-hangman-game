from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, wordvar=None, newmasked=None, hit=None, miss=None):
        
        if hit and miss:
            raise InvalidGuessAttempt()
            
        self.wordvar = wordvar
        self.newmasked = newmasked
                
        if wordvar:            
            self.oldmasked = self.wordvar.masked 
        else:
            self.oldmasked = None
        
        self.hit=hit
        self.miss=miss
        
    def is_hit(self):
        
        if self.hit is not None and not self.wordvar:
            return self.hit
       
        if (self.newmasked and self.oldmasked) and (self.newmasked != self.oldmasked):
            self.wordvar.masked = self.newmasked 
            return True
        else:
            return False

    def is_miss(self):

        if self.miss is not None and not self.wordvar:
            return self.miss         
        
        if (self.newmasked and self.oldmasked) and (self.newmasked == self.oldmasked):
            return True
        else:
            return False
        

class GuessWord(object):
    
    def __init__(self, answer):
        
        if not answer:
            raise InvalidWordException("Invalid Words")
            
        self.answer=answer.lower()
        self.masked = '*'*len(self.answer)
        
    def perform_attempt(self, guess):
        
        if not guess:
            raise InvalidWordException("Invalid Words")
        
        if len(guess) > 1:
            raise InvalidGuessedLetterException("Only one letter to guess")
                       
        result_str=''
        for idx, letter in enumerate(self.answer):
            if guess.lower()==letter:
                result_str+=self.answer[idx]
            else:
                result_str+=self.masked[idx]

        return GuessAttempt(guess, wordvar=self, newmasked=result_str)
        

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None,number_of_guesses=5):
        if word_list is None:
            self.word_list=self.WORD_LIST
        else:
            self.word_list=word_list
            
        self.remaining_misses = number_of_guesses
        self.previous_guesses=[]
        
        random_word = HangmanGame.select_random_word(self.word_list)

        self.word = GuessWord(random_word)

    @classmethod
    def select_random_word(cls, l_words):        
        if not l_words:
            raise InvalidListOfWordsException("Invalid List of Words")        
        return random.choice(l_words)    
    
    def is_finished(self):
        if self.remaining_misses==0 or self.word.answer==self.word.masked:
            return True
        else:
            return False    
    
    def is_lost(self):
        if self.word.answer!=self.word.masked and self.remaining_misses==0:
            return True
        else:
            return False

    def is_won(self):
        if self.word.answer==self.word.masked:
            return True
        else:
            return False
    
    def guess(self,answer):

        if self.is_finished():
            raise GameFinishedException

        l_answer = answer.lower()
        
        if l_answer not in self.previous_guesses:
            self.previous_guesses.append(l_answer)
            
        result=self.word.perform_attempt(l_answer)
            
        if result.is_miss():
            self.remaining_misses -= 1
            
        if result.is_hit() and self.is_won():
            raise GameWonException()
                            
        if self.is_lost():
            raise GameLostException()
                
        return result
                

        