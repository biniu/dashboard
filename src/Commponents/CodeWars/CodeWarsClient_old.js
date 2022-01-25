import React from 'react';
import {Col, Container, Row} from "react-bootstrap";

import LangInfo from "./LangInfo"
import StreaksView from "./StreaksView";

import {CircularProgressbar} from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';


import './CodeWars.css'
import data from "bootstrap/js/src/dom/data";

class CodeWarsClient extends React.Component {

    constructor(props) {
        super(props);
        // this.URI = [
        //     '/code_wars/UserStatistics/',
        //     '/code_wars/UserInfo/'
        //     ]
        // this.URI = 'http://127.0.0.1:8000/code_wars/UserStatistics/'
        // this.URI = 'https://www.codewars.com/api/v1/users/biniu'
        this.state = {
            UserStatistics: [],
            UserInfo: [],
        };
    }

    fetchData(url) {
        fetch(url)
            .then(async response => {
                const data = await response.json();

                if (!response.ok) {
                    const error = (data && data.message) || response.statusText;
                    return Promise.reject(error);
                }

                // this.setState({ UserStatistics: data.results[0] })
                return data
            })
            .catch(error => {
                // this.setState({ errorMessage: error.toString() });
                console.error('There was an error!', error);
                throw error.toString()
            });
    }

    componentDidMount() {
        try {
            console.log(this.fetchData('/code_wars/UserStatistics/'))
            this.setState({
                UserStatistics: this.fetchData('/code_wars/UserStatistics/')
            })
        } catch (e) {
            console.error(e);
        }

    }

    UserDetails() {
        console.log(this.state.UserStatistics)
        return (
            <table className={"codeWarsTable"}>
                <tr>
                    <td className={"cwTD"}> -> User name:</td>
                    <td className={"cwTD"}>{this.state.UserStatistics['username']}</td>
                </tr>
                <tr>
                    <td className={"cwTD"}> -> Honor:</td>
                    <td className={"cwTD"}>{this.state.UserStatistics['honor']}</td>
                </tr>
                <tr>
                    <td className={"cwTD"}> -> Position:</td>
                    <td className={"cwTD"}>{this.state.UserStatistics['leaderboardPosition']}</td>
                </tr>
            </table>
        )
    }

    render() {
        const percentage = 66;

        return (
            <Container fluid className={"codeWars"}>
                <Row className={"rowBorder"}>
                    CodeWars
                </Row>
                <Row className={"rowBorder"}>
                    <Col>
                        <Row className={"rowBorder"}>
                            {this.UserDetails()}
                        </Row>
                        <Row className={"rowBorder"}>
                            <StreaksView/>
                        </Row>
                    </Col>

                    <Col>
                        <Row className={"rowBorder"}>
                            {/*<LangInfo langDetails={this.state.data['ranks']}/>*/}
                        </Row>
                        <Row className={"rowBorder"}>
                            <CircularProgressbar value={percentage} text={`${percentage}%`}
                            />


                            {/*<LangInfo langDetails={this.state.data['ranks']}/>*/}
                        </Row>
                    </Col>
                </Row>
            </Container>
        )
    }
}

export default CodeWarsClient;
