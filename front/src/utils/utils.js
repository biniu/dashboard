import React, {useCallback, useEffect, useState} from "react";
import axios from "axios";

export function getTodayDate() {
    const t = new Date();
    const date = ('0' + t.getDate()).slice(-2);
    const month = ('0' + (t.getMonth() + 1)).slice(-2);
    const year = t.getFullYear();
    return `${year}-${month}-${date}`;
}

export function getYesterdayDate() {
    const t = new Date();
    t.setDate(t.getDate() - 1)

    const date = ('0' + t.getDate()).slice(-2);
    const month = ('0' + (t.getMonth() + 1)).slice(-2);
    const year = t.getFullYear();
    return `${year}-${month}-${date}`;
}

export function Request(url, onlyResults=true) {
    console.log("Request for URL [" + url + "]")
    let [data, setData] = useState('');
    const fetchData = useCallback(() => {
        axios({
            "method": "GET",
            "url": url,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then((response) => {
                setData(response.data)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [])
    React.useEffect(() => {
        fetchData()
    }, [fetchData])

    console.log(data)
    if(onlyResults) {
        return data['results']
    }
    return data;
}
