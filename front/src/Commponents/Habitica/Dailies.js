import React from "react";

import {Request} from "../../utils/utils";


export default function Dailies() {

    const url = "http://127.0.0.1:8000/habitica/Dailys"
    const data = Request(url, false)

    let todos_not_done = <></>

    console.log(data['results'])

    if(data['results']) {

        const not_done = data['results'].filter(todo => !todo.completed)

        todos_not_done = not_done.map((todo) => (
            <tr className={todo.priority === 1 ? "todoEntryTRP1" : "todoEntryTR"}>
                <td>
                    ▷ {todo.id}
                </td>
                <td className={"todoEntryTD"}>
                    {todo.priority}
                </td>
                <td className={"todoEntryTD"}>
                    {todo.text}
                </td>
            </tr>
        ))
    }

    return (
        <>
            <div className={"todoHeader"}>
                Dailys
            </div>
            <table>
                {todos_not_done}
            </table>
        </>
    )
}