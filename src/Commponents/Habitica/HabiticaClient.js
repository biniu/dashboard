import React from 'react';
import {Col, Container, Row} from "react-bootstrap";

import {CircularProgressbar} from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

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
                <li>
                    {tasksList['data'][i]['text']}
                </li>
            ))
        }

        const habitsList = this.state.data['habits']
        let habits = []

        if (habitsList) {
            habits = Object.keys(habitsList['data']).map((keyName, i) => (
                <li>
                    {habitsList['data'][i]['text']}
                </li>
            ))
        }

        const dailysList = this.state.data['dailys']
        let dailys = []

        if (dailysList) {
            dailys = Object.keys(dailysList['data']).map((keyName, i) => (
                <li>
                    {dailysList['data'][i]['text']}
                </li>
            ))
        }

        return (
            <Container fluid>
                <Row className={"rowBorder"}>
                    Tasks
                    <ul>
                    {tasks}
                    </ul>
                </Row>
                <Row className={"rowBorder"}>
                    Habits
                    <ul>
                        {habits}
                    </ul>
                </Row>
                <Row className={"rowBorder"}>
                    Dailys
                    <ul>
                        {dailys}
                    </ul>
                </Row>
            </Container>
        )
    }
}

export default HabiticaClient;
