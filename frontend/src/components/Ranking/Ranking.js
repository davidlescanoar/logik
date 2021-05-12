import React, {Component} from 'react';
import Table from "../Table/Table";
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import API from "../../API";
import Button from '@material-ui/core/Button';

const token = process.env.REACT_APP_TOKEN;

export default class Ranking extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            table: {
                rows: [],
                columns: [],
                order: 'asc',
                orderBy: 'rank',
            }
        };
    }

    getProblemTable(problems) {
        let problemList = [];
        for (var i = 0; i < problems.length; i++) {
            let rank = problems[i].rank;
            let user = problems[i].user;
            let score = problems[i].score;
            var problem = [
                [rank, null],
                [user, null],
                [score, null],
            ];
            problemList.push(problem);
        }
        return problemList;
    }

    getTable = async event => {
        const response = await API.get("ranking/", {headers: {'Authorization': token}});
        const problemList = this.getProblemTable(response.data);
        this.setState({
            table: {
                ...this.state.table,
                rows: problemList,
                columns: [
                    {
                        id: 'rank',
                        numeric: true,
                        disablePadding: true,
                        label: '#'
                    },
                    {
                        id: 'user',
                        numeric: false,
                        disablePadding: false,
                        label: 'Usuario'
                    },
                    {
                        id: 'score',
                        numeric: true,
                        disablePadding: false,
                        label: 'Puntaje'
                    },
                ],
            }
        });

    };

    componentDidMount() {
        this.getTable();
    }

    render() {
        return (
            <div>
                <Typography variant="h5" gutterBottom>
                    Ranking
                </Typography>
                <Table source={this.state.table}/>
            </div>
        )
    }
}