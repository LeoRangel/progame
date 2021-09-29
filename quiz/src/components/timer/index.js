import React, { Component } from 'react'

import {
    Contador,
    Container,
    FooterWrapper
} from "./styles";

class Timer extends Component{
    
    constructor (props){
        super(props)
        this.state = {
            count: 0,
            questao: 0
        }
    }

    render(){
        const {count} = this.state
        const {questao} = this.state
        if (count > 0) {
            return (
                <Container>
                    <FooterWrapper>
                        <Contador>
                            <div className="numero">{count}</div>
                            {/* <small className="numero">( Tempo para pontuar na questão: {count} )</small> */}
                            {/* <small className="ml-3">Questao: {questao}</small> */}
                        </Contador>
                    </FooterWrapper>
                </Container>
            )
        } else {
            return (
                <Container>
                    <FooterWrapper>
                        <Contador>
                            <div className="nao-pontuar">
                                Tempo esgotado: você não ganhará pontos :(
                            </div>
                        </Contador>
                    </FooterWrapper>
                </Container>
            )
        }
    }

    // setInterval
    // clearInterval
    componentDidMount(){
        const {startCount, questao} = this.props
        this.setState({
            count: startCount,
            questao: questao
        })
        this.doIntervalChange()
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.questao !== nextProps.questao) {
            if (this.myInterval) {
                clearInterval(this.myInterval)
            }
            const {startCount, questao} = this.props
            this.setState({
                count: startCount,
                questao: questao
            })
            this.doIntervalChange()
        }
    }

    doIntervalChange = () => {
        this.myInterval = setInterval(() => {
            const {count} = this.state
            if (count > 0) {
                this.setState(prevState => ({
                    count: prevState.count - 1
                }))
            } else {
                clearInterval(this.myInterval)
            }
        }, 1000)
    }

    componentWillUnmount(){
        clearInterval(this.myInterval)
    }

}

export default Timer;