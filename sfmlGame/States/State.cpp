//
// Created by ek on 26.03.2022.
//

#include "State.h"


State::State( sf::RenderWindow *window, std::map<std::string, int> * suppoertedKeys ) {
    this->window = window;
    this->supportedKeys = suppoertedKeys;
    this->quit = false;
}

State::~State() {

}

void State::checkForQuit() {
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key(this->keybinds.at("CLOSE")))){
        this->quit = true;
    }

}
const bool & State::getQuit() const {
    return this->quit;
}

void State::endState() {

}

void State::updateMousePositions() {
    this->mousePosScreen = sf::Mouse::getPosition();
    this->mousePosWindow = sf::Mouse::getPosition( *this->window );
    this->mousePosView = this->window->mapPixelToCoords( sf::Mouse::getPosition() );
}