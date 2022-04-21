//
// Created by ek on 26.03.2022.
//

#include "GameState.h"

GameState::GameState(sf::RenderWindow * window, std::map<std::string, int> * suppoertedKeys)
: State( window, suppoertedKeys ){
    this->initKeybinds();
}
GameState::~GameState() noexcept {

}


void GameState::initKeybinds() {


    std::fstream ifs("../../sndbx/Configs/gamestate_keybinds.txt");
    if (ifs.is_open()){
        std::string key = "";
        std::string key2 = "";

        while (ifs >> key >> key2){
            this->keybinds[key] = this->supportedKeys->at(key2);
        }
    }
    ifs.close();

}

void GameState::update(const float & dt) {
    this->updateMousePositions();
    this->updateInput(dt);
    this->player.update(dt);

}

void GameState::render(sf::RenderTarget* target  ) {

    if (!target)
        target = this->window;
    this->player.render( target );


}

void GameState::endState() {
    std::cout<< " Ending game state \n";
}

void GameState::updateInput(const float &dt) {
    this->checkForQuit();

    // Update player input
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key(this->keybinds.at("MOVE_LEFT"))))
        this->player.move(dt, -1.f, 0.f);
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key(this->keybinds.at("MOVE_RIGHT"))))
        this->player.move(dt, 1.f, 0.f);
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key(this->keybinds.at("MOVE_UP"))))
        this->player.move(dt, 0.f, -1.f);
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key(this->keybinds.at("MOVE_DOWN"))))
        this->player.move(dt, 0.f, 1.f);

}

void GameState::checkForQuit() {
}