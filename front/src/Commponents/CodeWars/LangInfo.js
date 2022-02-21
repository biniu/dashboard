import React, {useContext} from "react";

import './CodeWars.css'

import {Request} from "../../utils/utils";
import {UserID, UserName} from "./CodeWarsClient";


const LangDetails = (lang_obj) => {
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
        if (levels[i].score > lang_obj.score) {
            x = levels[i].score - levels[i - 1].score
            y = lang_obj.score - levels[i - 1].score
            percent = ((y / x) * 100).toFixed(1);
            break
        }
    }

    console.log("lang_obj")
    console.log(lang_obj)

     return (
        <>
            <td className={"cwTD"}>
                {lang_obj.name}:
            </td>
            <td className={"cwTD"}>
                {lang_obj.score}
            </td>
            <td className={"cwTD"}>
                {/*<ProgressBar now={percent} label={`${percent}%`} srOnly />*/}

                <progress max={x} value={y}> {percent} </progress>
                {percent}%
            </td>
        </>
    )
}


export default function LangInfo() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)

    const url_lang_list = "http://127.0.0.1:8000/CodeWars/LanguageScores/" + userID
    const lang_list = Request(url_lang_list, false)

    let langData = <tr/>

    if (lang_list) {

        const newest_score = lang_list.reduce((p, c) => p.last_update > c.last_update ? p : c);

        const newest_lang_list = lang_list.filter(function (lang) {
            return lang.last_update === newest_score.last_update
        });

        langData = newest_lang_list.map((lang) => (
            <tr>
                {LangDetails(lang)}
            </tr>
        ))
    }

        return (
        <table className={"codeWarsTable"}>
            {langData}
        </table>
    );
}
