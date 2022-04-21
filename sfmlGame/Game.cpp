//
// Created by ek on 26.03.2022.
//

#include "Game.h"


// Static Functions


// Initializer functions

void Game::initWindow() {
    /* create new SFML window */
    std::ifstream ifs("../../sndbx/Configs/config.txt");
    std::string title = "None";
    sf::VideoMode window_bounds(800, 600);
    unsigned framerate_limit = 120;
    bool vertical_sync_enabled = false;

    if (ifs.is_open()){
        std::getline(ifs, title);
        ifs >> window_bounds.width >> window_bounds.height;
        ifs >> framerate_limit;
        ifs >> vertical_sync_enabled;
    }
    ifs.close();


    this->window = new sf::RenderWindow( window_bounds, "C++ SFML" );
    this->window->setFramerateLimit(framerate_limit);
    this->window->setVerticalSyncEnabled(vertical_sync_enabled);
}


void Game::initKeys() {

    std::fstream ifs("../../sndbx/Configs/supported_keys.txt");
    if (ifs.is_open()){
        std::string key = "";
        int key_value = 0;

        while (ifs >> key >> key_value){
            this->supportedKeys[key] = key_value;
        }
    }
    ifs.close();

    this->supportedKeys.emplace("Escape", sf::Keyboard::Key::Escape);
    this->supportedKeys.emplace("A", sf::Keyboard::Key::A);
    this->supportedKeys.emplace("D", sf::Keyboard::Key::D);
    this->supportedKeys.emplace("W", sf::Keyboard::Key::W);
    this->supportedKeys.emplace("S", sf::Keyboard::Key::S);

    // Debug
    for(auto i: this->supportedKeys )
    {
        std::cout << i.first << " " << i.second << "\n";
    }

}



void Game::initStates() {
    this->states.push( new MainMenuState(this->window , &this->supportedKeys ) );
//    this->states.push( new GameState(this->window , &this->supportedKeys ) );
}

// Constructor/Destructor functions
Game::Game() {
    this->initWindow();
    this->initKeys();
    this->initStates();

}
Game::~Game() {

    delete this->window;
    while (!this->states.empty()) {
        delete this->states.top();
        this->states.pop();
    }

}

void Game::updateSFMLEvents() {
    while (this->window->pollEvent(this->sfEvent))
    {
       if (this->sfEvent.type == sf::Event::Closed)
                this->window->close();
    }
}

void Game::update() {
    this->updateSFMLEvents();
    if (! this->states.empty()) {
        this->states.top()->update(this->dt);
        if (this->states.top()->getQuit()){
            //
            this->states.top()->endState();
            delete this->states.top();
            this->states.pop();
        }

    }
    //Application End
    else{
        this->endApplication();
        this->window->close();
        this->endFlag = true;
    }

}

int Game::run() {
    this->updateDt();
    this->update();
    this->render();

    if (this->endFlag)
        return 0;
    return 1;
}
void Game::render() {
    this->window->clear();

    if (! this->states.empty())
        this->states.top()->render();

    this->window->display();
}

void Game::updateDt() {
    /* update the dt variable with the time it takes to render one frame */
    this->dt = this->dtClock.restart().asSeconds();

}
void Game::endApplication() {
    std::cout<< "ending application \n";
}
