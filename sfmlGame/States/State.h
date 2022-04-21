//
// Created by ek on 26.03.2022.
//

#ifndef INC_3DCG_RESEARCH_AND_IMPLEMENTATION_STATE_H
#define INC_3DCG_RESEARCH_AND_IMPLEMENTATION_STATE_H

#include "../Entity/Entity.h"

class State {
private:
protected:
    sf::RenderWindow * window;
    std::map<std::string, int>* supportedKeys;
    std::map<std::string, int> keybinds;
    bool quit;

    sf::Vector2i mousePosScreen;
    sf::Vector2i mousePosWindow;
    sf::Vector2f mousePosView;

    //Resources
    std::vector<sf::Texture> textures;


    //Functions
    virtual void initKeybinds() = 0;

public:
    State( sf::RenderWindow * window, std::map<std::string, int> * suppoertedKeys);
    virtual ~State();

    virtual void endState() = 0;
    virtual void updateMousePositions();
    virtual void updateInput( const float & dt) = 0;
    const bool& getQuit() const;
    virtual void checkForQuit() = 0;
    virtual void update( const float & dt) = 0;
    virtual void render(sf::RenderTarget* target = NULL ) = 0;
};


#endif //INC_3DCG_RESEARCH_AND_IMPLEMENTATION_STATE_H
