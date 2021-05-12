import React, {Component} from 'react';
import Table from "../Table/Table";
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import API from "../../API";
import Button from '@material-ui/core/Button';

const token = process.env.REACT_APP_TOKEN;

export default class Recommended extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            table: {
                rows: [],
                columns: [],
                order: 'desc',
                orderBy: 'score',
            }
        };
    }

    getProblemTable(problems) {
        let problemList = [];
        for (var i = 0; i < problems.length; i++) {
            let name = problems[i].name;
            let link = problems[i].link;
            let score = problems[i].score;
            var problem = [
                [name, link],
                [score, null],
            ];
            problemList.push(problem);
        }
        return problemList;
    }

    getTable = async event => {
        const response = await API.get("recommended/?username="+this.props.username, {headers: {'Authorization': token}});
        const problemList = this.getProblemTable(response.data);
        this.setState({
            table: {
                ...this.state.table,
                rows: problemList,
                columns: [
                    {
                        id: 'name',
                        numeric: false,
                        disablePadding: true,
                        label: 'Nombre'
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
                    Recomendados
                </Typography>
                <Table source={this.state.table}/>
            </div>
        )
    }
}