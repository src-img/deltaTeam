#include <stdio.h>
#include <string>
#include <limits>
#include <chrono> // for testing only
#include <thread> //for testing only

#include <random> // for testing only
#include <iostream> // for testing only

enum class state {addNote, addRest, duration};

std::string composition = "|";
state button;
void setNoteSizeLimit(const int&, int&);


int main() {

    std::random_device rd; // for testing only
    std::mt19937 gen(rd()); // for testing only
    std::uniform_int_distribution<> distrib(0, 10);  // for testing only

    std::string noteArray[] = {"S","E","E.","Q","Q+S","Q.","Q.+S","H","H+S","H+E","H+E.","H.","H.+S","H.+E","H.+E.","W"};
    std::string restArray[] = {"s","e","e.","q","q+s","q.","q.+s","h","h+s","h+e","h+e.","h.","h.+s","h.+e","h.+e.","w"};

    int sixteenth = 1;
    int noteSizeLimit = 15;
    int noteSize = 0;
    std::string* arrayPtr = restArray;
    
    for(int i = 0; i< 160; ++i) {
        int randomNumber = distrib(gen); // for testing only
        if (randomNumber == 0) button = state::addNote; // for testing only
        else if (randomNumber == 1) button = state::addRest; // for testing only
        else button = state::duration; // for testing only

        
        if (button != state::duration || ((sixteenth % 16) == 0) || (noteSize == noteSizeLimit)){
            composition += arrayPtr[noteSize];
            if(button == state::duration && arrayPtr == noteArray) 
                composition += "+";
            if ((sixteenth % 16) == 0)
                composition += "|";
            setNoteSizeLimit(sixteenth, noteSizeLimit); 
            if (button != state::duration)
                (button == state::addNote) ? arrayPtr = noteArray : arrayPtr = restArray; 
            noteSize = 0;
            button = state::duration;
        }
        else 
            ++noteSize; 
        ++sixteenth;              
    }
    std::cout << composition << std::endl;
}


void setNoteSizeLimit(const int &sixteenth, int &noteSizeLimit){
            switch(sixteenth % 4){
                case 0: 
                    switch((sixteenth%16)/4){
                        case 0: 
                            noteSizeLimit = 15; break;
                        case 1: 
                            noteSizeLimit = 11; break;
                        case 2: 
                            noteSizeLimit = 7; break;
                        case 3: 
                            noteSizeLimit = 3; break;
                    } break;
                case 1:
                    noteSizeLimit = 1; break;
                case 2:
                    noteSizeLimit = 1; break;
                case 3:
                    noteSizeLimit = 0; break;
            }
}
