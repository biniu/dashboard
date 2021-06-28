import React from 'react';
import {Col, Row} from "react-bootstrap";

class CodeWarsClient extends React.Component {

    constructor(props) {
        super(props);
        this.URI = 'http://localhost:3001/users/biniu'
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

    LangDetails(langObj, langName) {

        const levels = [
            {name: "8 kyu", score: 0},
            {name: "7 kyu", score: 20},
            {name: "6 kyu", score: 76},
            {name: "5 kyu", score: 229},
            {name: "4 kyu", score: 643},
            {name: "3 kyu", score: 1768},
            {name: "2 kyu", score: 4829},
            {name: "1 kyu", score: 13147},
            {name: "1 dan", score: 35759},
            {name: "2 dan", score: 97225},
        ]
        let percent = 0
        let x, y = 0
        for (let i = 0; i < levels.length; i++) {
            if (levels[i].score > langObj.score) {
                x = levels[i].score - levels[i - 1].score
                y = langObj.score - levels[i - 1].score
                percent = ((y / x) * 100).toFixed(1);
                break
            }
        }

        return (
            <>
                <td className={"cwTD"}
                    style={{color: langObj.color}}
                >{langName}:
                </td>
                <td className={"cwTD"}
                    style={{color: langObj.color}}
                >{langObj.score}</td>
                <td className={"cwTD"}
                    style={{color: langObj.color}}
                >{langObj.name}</td>
                <td className={"cwTD"}
                    style={{color: langObj.color}}
                >
                    <progress max={x} value={y}> {percent} </progress>
                    {percent}
                </td>

            </>
        )
    }

    LangOverview() {
        const ranks = this.state.data['ranks']
        let out = []

        if (ranks) {
            out = Object.keys(ranks['languages']).map((keyName, i) => (
                <tr>
                    {this.LangDetails(ranks['languages'][keyName], keyName)}
                </tr>
            ))
        }

        return (
            <>{out}</>
        )
    }

    render() {
        return (
            <Row className={"codeWars"}>
                <Row>
                    CodeWars
                </Row>
                <Row>
                    <Col>
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
                    </Col>

                    <Col>
                        {this.LangOverview()}
                    </Col>
                </Row>
            </Row>
        )
    }
}

export default CodeWarsClient;
