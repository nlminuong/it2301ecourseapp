import axios from "axios";

export const endpoints = {
    categories: "/categories/",
    courses: "/courses"
};

export default axios.create({
    baseURL: "http://192.168.223.33:8000/"
});