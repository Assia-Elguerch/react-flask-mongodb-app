import axios from 'axios'
import { API_URL } from './config'

// API_URL est automatiquement détecté selon l'environnement (local ou Docker)

export const getList = () => {
    return axios
        .get(`${API_URL}/api/tasks`, {
            headers: { 'Content-type': 'application/json' }
        })
        .then(res => {
            var data = []
            Object.keys(res.data).forEach(function (key) {
                var val = res.data[key]
                data.push([val.title, val._id])
            })
            return data
        })
        .catch(error => {
            console.error('Error fetching tasks:', error)
            return []
        })
}

export const addToList = term => {
    return axios
        .post(
            `${API_URL}/api/task`,
            {
                title: term
            },
            {
                headers: { 'Content-type': 'application/json' }
            }
        )
        .then((response) => {
            console.log(response)
        })
        .catch(error => {
            console.error('Error adding task:', error)
        })
}

export const deleteItem = term => {
    return axios
        .delete(`${API_URL}/api/task/${term}`, {
            headers: { 'Content-type': 'application/json' }
        })
        .then((response) => {
            console.log(response)
        })
        .catch((error) => {
            console.error('Error deleting task:', error)
        })
}

export const updateItem = (term, id) => {
    return axios
        .put(`${API_URL}/api/task/${id}`, {
            title: term
        }, {
            headers: { 'Content-type': 'application/json' }
        })
        .then((response) => {
            console.log(response)
        })
        .catch(error => {
            console.error('Error updating task:', error)
        })
}