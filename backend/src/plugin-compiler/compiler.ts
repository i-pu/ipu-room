// =========================
// compiler.ts
//
// Copyright (c) 2019 i-pu
// =========================

const fs = require('fs')
const RawCounter = fs.readFileSync('@plugin/counter.ipl', { encoding: 'utf-8' })

export const compilePlugin = async (iplRawString: string): Promise<{ template: string, functions: string }> => {
  try {
    const tepmlateMatchresult = iplRawString.match(/.*\<template\>(.*)\<\/template\>.*\<script\>(.*)\<\/script\>.*/s)
  
    if (!tepmlateMatchresult) {
      throw '[Plugin Compiler] Illegal format.'
    }

    const [template, rawScript] = [tepmlateMatchresult[1], tepmlateMatchresult[2]]

    const scriptResult = rawScript.match(/export default.*?{(.*)}/s)

    if (!scriptResult) {
      throw '[Plugin Compiler] Functions not found.'
    }

    const functions = scriptResult[1]

    return {
      template, functions: `({${functions}})`
    }
  } catch (error) {
    throw error
  }
}

const __compilePlugin_test__ = async () => {
  console.log(RawCounter)

  // console.log(tsc.compileString(`
  // class { 
  //   awesome: boolean = true
  // }
  // `, null, null, (e: any) => {
  //   if (e) {
  //     console.log(e)
  //   }
  // }))
}

__compilePlugin_test__()