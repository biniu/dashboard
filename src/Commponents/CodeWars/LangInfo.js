import React, {useCallback, useContext, useState} from "react";
import axios from "axios";

import './CodeWars.css'
import {UserName} from "./CodeWarsClient";
import {Request} from "../../utils/utils";


const LangDetails = (lang_obj, lang_details) => {
    const lang_info = lang_details.filter(
        lang_details => lang_details.lang_id === lang_obj.id).slice(-1)[0]

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
        if (levels[i].score > lang_info.score) {
            x = levels[i].score - levels[i - 1].score
            y = lang_info.score - levels[i - 1].score
            percent = ((y / x) * 100).toFixed(1);
            break
        }
    }

    return (
        <>
            <td className={"cwTD"} style={{color: lang_info.color}}>
                {lang_obj.name}:
            </td>
            <td className={"cwTD"} style={{color: lang_info.color}}>
                {lang_info.score}
            </td>
            <td className={"cwTD"} style={{color: lang_info.color}}>
                {/*<ProgressBar now={percent} label={`${percent}%`} srOnly />*/}

                <progress max={x} value={y}> {percent} </progress>
                {percent}%
            </td>
        </>
    )
}

export default function LangInfo() {
    // const userName = useContext(UserName)
    const url_lang_list = "http://127.0.0.1:8000/code_wars/LanguageInfo/"
    const lang_list = Request(url_lang_list, false)

    const url_lang_details = "http://127.0.0.1:8000/code_wars/LanguageScores/"
    console.log(url_lang_details)
    const lang_data = Request(url_lang_details, false)
    console.log(lang_data)

    let langData = <tr/>

    if (lang_list['results'] && lang_data['results']) {
        console.log(lang_list['results'])
        langData = lang_list['results'].map((lang) => (
            <tr>
                {LangDetails(lang, lang_data['results'])}
            </tr>
        ))
    }

    return (
        <table className={"codeWarsTable"}>
            {langData}
        </table>
    );
}
