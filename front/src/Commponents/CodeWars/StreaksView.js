import React from 'react';
import {Col, Row} from "react-bootstrap";

class StreaksView extends React.Component {

    constructor(props) {
        super(props);
        this.URI = 'http://localhost:3001/users/biniu'
        // this.URI = 'https://www.codewars.com/api/v1/users/biniu'
        this.state = {data: []};
        this.today = new Date();
        this.month = this.today.toLocaleString('default', { month: 'long' });
        // this.today = new Date(2021, 7, 15);
        // this.today = new Date(2021, 1, 15);
    }

    fillWeek(startDate, endDate) {
        let out = []
        for (let tmpDate = startDate; tmpDate <= endDate; tmpDate.setDate(tmpDate.getDate() + 1)) {
            const toAdd = tmpDate.getMonth() === this.today.getMonth() ? tmpDate.getDate() : 0
            out.push(<td>{toAdd}</td>)
        }
        return (out)
    }

    generateWeeks() {
        let out = []

        const firstDay = new Date(this.today.getFullYear(), this.today.getMonth(), 0);
        const lastDay = new Date(this.today.getFullYear(), this.today.getMonth() + 1, 0);

        let startDate = firstDay
        while (startDate < lastDay) {
            let tmpDate = startDate
            const weekFirstDay = new Date(tmpDate.setDate(tmpDate.getDate() - tmpDate.getDay() + 1));
            tmpDate = startDate
            const weekLastDay = new Date(tmpDate.setDate(tmpDate.getDate() - tmpDate.getDay() + 7));

            out.push(
                <tr className={'streaksTr'}>
                    {this.fillWeek(weekFirstDay, weekLastDay)}
                </tr>
            )
            startDate = weekLastDay
        }

        return (out)
    }

    render() {
        return (
            <>
                <table className={'streaksTable'}>
                    <tr className={'streaksTr'}>
                        <th colspan="7" className={'streaksTh'}>{this.month}</th>
                    </tr>
                    <tr className={'streaksTr'}>
                        <td className={'streaksTd'}>M</td>
                        <td className={'streaksTd'}>T</td>
                        <td className={'streaksTd'}>W</td>
                        <td className={'streaksTd'}>T</td>
                        <td className={'streaksTd'}>F</td>
                        <td className={'streaksTd'}>S</td>
                        <td className={'streaksTd'}>S</td>
                    </tr>

                    {this.generateWeeks()}
                </table>
            </>
        )
    }
}

export default StreaksView;
