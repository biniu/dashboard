import React, {useCallback, useState} from "react";
import axios from "axios";

import './CodeWars.css'


function LangDetails(langObj, langName) {
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

export default function LangInfo() {
    let [userData, setUserData] = useState('');
    const fetchData = useCallback(() => {
        axios({
            "method": "GET",
            "url": "http://localhost:3001/codeWarsUser",
        })
            .then((response) => {
                setUserData(response.data)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [])
    React.useEffect(() => {
        fetchData()
    }, [fetchData])

    let data = <tr/>

    if(userData['ranks']) {
        console.log(userData['ranks']['languages'])
        data = Object.keys(userData['ranks']['languages']).map((keyName, i) => (
            <tr>
                {LangDetails(userData['ranks']['languages'][keyName], keyName)}
            </tr>
        ))
    }

    return (
        <table className={"codeWarsTable"}>
            {data}
        </table>
    );
}
