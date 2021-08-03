import React from 'react';
import {Col, Container, Row} from "react-bootstrap";

import {CircularProgressbar} from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

import './HabiticaClient.css'

class HabiticaClient extends React.Component {

    constructor(props) {
        super(props);
        this.URI = 'http://localhost:3001/habitica/'
        this.state = {data: []};
    }

    // componentDidMount() {
    //     fetch(this.URI)
    //         .then(response => {
    //             return response.json();
    //         }).then(result => {
    //         this.setState({
    //             data: result
    //         });
    //     });
    // }

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
        const tasksList = this.state.data['todos']
        let tasks = []

        if (tasksList) {
            tasks = Object.keys(tasksList['data']).map((keyName, i) => (
                <tr>
                    {tasksList['data'][i]['text']}
                </tr>
            ))
        }

        const habitsList = this.state.data['habits']
        let habits = []

        if (habitsList) {
            habits = Object.keys(habitsList['data']).map((keyName, i) => (
                <tr>
                    {habitsList['data'][i]['text']}
                </tr>
            ))
        }

        const dailiesList = this.state.data['dailies']
        let dailies = []

        if (dailiesList) {
            dailies = Object.keys(dailiesList['data']).map((keyName, i) => (
                <tr>
                    <td>
                        {dailiesList['data'][i]['text']}
                    </td>
                    <td>
                        STATUS
                    </td>
                </tr>
            ))
        }

        return (
            <Container fluid className={"habiticaClient"}>
                <Row className={"rowBorder"}>
                    <Col>
                        Tasks
                        <table>
                            {tasks}
                        </table>
                    </Col>

                    <Col>
                        <Row className={"rowBorder"}>
                            Dailies
                            <table>
                                {dailies}
                            </table>
                        </Row>

                        <Row className={"rowBorder"}>
                            Habits
                            <table>
                                {habits}
                            </table>
                        </Row>
                    </Col>
                </Row>
            </Container>
        )
    }
}

export default HabiticaClient;
