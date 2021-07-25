import React from 'react';
import {Col, Container, Row} from "react-bootstrap";

import LangInfo from "./LangInfo"
import StreaksView from "./StreaksView";

import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';


import './CodeWars.css'

class CodeWarsClient extends React.Component {

    constructor(props) {
        super(props);
        this.URI = 'http://localhost:3001/codeWars'
        // this.URI = 'https://www.codewars.com/api/v1/users/biniu'
        this.state = {data: []};
    }

    componentDidMount() {
        fetch(this.URI)
            .then(response => {
                return response.json();
            }).then(result => {
            this.setState({
                data: result
            });
        });
    }

    UserDetails() {
        return (
            <table className={"codeWarsTable"}>
                <tr>
                    <td className={"cwTD"}> -> User name:</td>
                    <td className={"cwTD"}>{this.state.data['username']}</td>
                </tr>
                <tr>
                    <td className={"cwTD"}> -> Honor:</td>
                    <td className={"cwTD"}>{this.state.data['honor']}</td>
                </tr>
                <tr>
                    <td className={"cwTD"}> -> Position:</td>
                    <td className={"cwTD"}>{this.state.data['leaderboardPosition']}</td>
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
                        <LangInfo langDetails={this.state.data['ranks']}/>
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
