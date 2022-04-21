//
// Created by ek on 27.03.2022.
//

#include "MainMenuState.h"

MainMenuState::MainMenuState(sf::RenderWindow * window, std::map<std::string, int> * suppoertedKeys)
        : State( window, suppoertedKeys ){
    this->initFonts();
    this->initKeybinds();
    this->background.setSize( sf::Vector2f (window->getSize().x,  window->getSize().y ));
    this->background.setFillColor(sf::Color::Magenta );
}
MainMenuState::~MainMenuState() noexcept {

}


void MainMenuState::initKeybinds() {


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

void MainMenuState::update(const float & dt) {
    this->updateMousePositions();
    this->updateInput(dt);

    system("cls");
    std::cout<< this->mousePosView.x << " " << this->mousePosView.y <<"\n";


}

void MainMenuState::render(sf::RenderTarget* target  ) {

    if (!target)
        target = this->window;

    target->draw(this->background);
    //this->player.render( target );


}

void MainMenuState::endState() {
    std::cout<< " Ending game state \n";
}

void MainMenuState::updateInput(const float &dt) {
    this->checkForQuit();


    //if (sf::Keyboard::isKeyPressed(sf::Keyboard::G))


}

void MainMenuState::checkForQuit() {
}

void MainMenuState::initFonts() {
    if( !this->font.loadFromFile( "../../sndbx/Fonts/Lato-Regular.ttf"))
        throw("ERROR::MAINMENUSTATE::COULD NOT LOAD FONT");
}