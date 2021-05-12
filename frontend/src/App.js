import logo from './logo.svg';
import React, {Component} from 'react';
import {BrowserRouter, Route, Switch, Redirect} from 'react-router-dom';
import Home from './components/Home/Home';
import Problems from './components/Problems/Problems'
import Login from './components/Login/Login'
import Menu from "./components/Menu/Menu";
import {Container} from "react-bootstrap";
import Recommended from "./components/Recommended/Recommended";
import Ranking from "./components/Ranking/Ranking";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            sectionID: 1,
        };
        this.setSection = this.setSection.bind(this);
    }

    setSection(index) {
        this.setState({sectionID: index});
    }

    render() {
        const user = 'DavidLescano';
        const sections = [<Home/>, <Problems username={user}/>, <Recommended username={user}/>, <Ranking username={user}/>];
        return (
            <BrowserRouter>
                <Container>
                    <div>
                        <Menu onChange={this.setSection}/>
                        {sections[this.state.sectionID]}
                        {/*
                            <Switch>
                                <Route
                                    path="/"
                                    component={Home}
                                    exact/>
                                <Route
                                    path="/problems"
                                    component={Problems}
                                    exact/>
                                <Route
                                    path="/login"
                                    component={Login}
                                    exact/>
                                {//<Route component={PageError}/>}
                            </Switch>
                        */}
                    </div>
                </Container>
            </BrowserRouter>
        );
    }
}

export default App;
