//
// Created by ek on 26.03.2022.
//

#ifndef INC_3DCG_RESEARCH_AND_IMPLEMENTATION_GAMESTATE_H
#define INC_3DCG_RESEARCH_AND_IMPLEMENTATION_GAMESTATE_H

#include "State.h"
class GameState : public State {
private:
    Entity player;

    //Functions
    void initKeybinds();

public:

    GameState(sf::RenderWindow * window, std::map<std::string, int> * suppoertedKeys);
    virtual ~GameState();
    void endState();

    void checkForQuit();

    void updateInput(const float & dt);

    void update( const float & dt);
    void render(sf::RenderTarget* target = NULL );

};


#endif //INC_3DCG_RESEARCH_AND_IMPLEMENTATION_GAMESTATE_H
