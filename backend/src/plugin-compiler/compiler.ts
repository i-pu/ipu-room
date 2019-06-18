// =========================
// compiler.ts
//
// Copyright (c) 2019 i-pu
// =========================

import { readFileSync } from 'fs'
// @ts-ignore
import { compileString, compile } from 'typescript-compiler'
import { parse } from 'node-html-parser'

export const compilePlugin = async (iplRawString: string): Promise<{ template: string, functions: string }> => {
  try {
    const plugin = parse(iplRawString)

    console.log(plugin.toString())

    return {
      template: '', functions: `({})`
    }
  } catch (error) {
    throw error
  }
}

export const __compilePlugin_test__ = async () => {
  const RawCounter = readFileSync(__dirname + '/../examples/counter.ipl', { encoding: 'utf-8' })
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

// __compilePlugin_test__()