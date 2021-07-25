import React from 'react';
import {ProgressBar} from "react-bootstrap";

class LangInfo extends React.Component {

    constructor(props) {
        super(props);
        // this.langDetails = props
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
        let x,y = 0
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
                    {/*<ProgressBar now={percent} label={`${percent}%`} srOnly />*/}

                    <progress max={x} value={y}
                    > {percent} </progress>
                    {percent}%
                </td>

            </>
        )
    }

    render() {
        const ranks = this.props.langDetails
        let out = []

        if (ranks) {
            out = Object.keys(ranks['languages']).map((keyName, i) => (
                <tr>
                    {this.LangDetails(ranks['languages'][keyName], keyName)}
                </tr>
            ))
        }

        return (
            <table>
                {out}
            </table>
        )
    }
}

export default LangInfo;
