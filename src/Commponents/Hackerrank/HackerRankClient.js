import React from 'react';
import {Col, Container, Row} from "react-bootstrap";

import './HackerRankClient.css'

class HackerRankClient extends React.Component {

    constructor(props) {
        super(props);
        this.URI = 'http://localhost:3001/hackerrank/'
        this.state = {data: []};
    }


    async componentDidMount() {
        try {
            const response = await fetch(this.URI);
            const json = await response.json();
            this.setState({ data: json });
            if (!response.ok) {
                throw Error(response.statusText);
            }
        } catch (error) {
            console.log(error);
        }
    }


    render() {
        const scoresList = this.state.data['scores_elo']
        let scores = []
        console.log(scoresList)

        if (scoresList) {
            scores = Object.keys(scoresList).map(getScoreElem)

            function getScoreElem(keyName) {
                if (scoresList[keyName]['practice'] &&
                    scoresList[keyName]['practice']['score'] > 0) {
                    return (
                        <tr>
                            <td>
                                {scoresList[keyName]['name']}
                            </td>
                            <td>
                                {scoresList[keyName]['practice']['score']}
                            </td>
                        </tr>
                    )
                }
            }
        }
        return (
            <Container fluid className={'HackerRankClient'}>
                <Row>
                HackerRank
                <table>
                    {scores}
                </table>
                </Row>
            </Container>
        )
    }
}

export default HackerRankClient;
