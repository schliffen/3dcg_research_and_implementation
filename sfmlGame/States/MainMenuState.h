//
// Created by ek on 27.03.2022.
//

#ifndef INC_3DCG_RESEARCH_AND_IMPLEMENTATION_MAINMENUSTATE_H
#define INC_3DCG_RESEARCH_AND_IMPLEMENTATION_MAINMENUSTATE_H

#include "GameState.h"
#include "../Resources/Button.h"

class MainMenuState : public State {

private:
    //variables
    sf::RectangleShape background;
    sf::Font font;

    //Functions
    void initFonts();
    void initKeybinds();

public:

    MainMenuState(sf::RenderWindow * window, std::map<std::string, int> * suppoertedKeys);
    virtual ~MainMenuState();
    void endState();

    void checkForQuit();

    void updateInput(const float & dt);

    void update( const float & dt);
    void render(sf::RenderTarget* target = NULL );




};


#endif //INC_3DCG_RESEARCH_AND_IMPLEMENTATION_MAINMENUSTATE_H
