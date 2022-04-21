//
// Created by ek on 26.03.2022.
//

#ifndef INC_3DCG_RESEARCH_AND_IMPLEMENTATION_GAME_H
#define INC_3DCG_RESEARCH_AND_IMPLEMENTATION_GAME_H


#include "States/MainMenuState.h"
#include "States/GameState.h"


class Game {
private:
    //Variables
    sf::RenderWindow* window;
    sf::Event sfEvent;
    sf::Clock dtClock;
    float dt;
    std::stack <State*> states;

    std::map <std::string , int> supportedKeys;

    // game End flag
    bool endFlag = false;

    // Initialization
    void initWindow();
    void initKeys();
    void initStates();




public:
    Game();
    virtual ~Game();

    // Functions

    // Regular
    void endApplication();

    //update
    void updateDt();
    void updateSFMLEvents();
    void update();
    //render
    void render();

    //core
    int run();


};


#endif //INC_3DCG_RESEARCH_AND_IMPLEMENTATION_GAME_H
