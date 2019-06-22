// =========================
// compiler.ts
//
// Copyright (c) 2019 i-pu
// =========================

// @ts-ignore
import { compileString } from 'typescript-compiler'
import { parse, NodeType, HTMLElement } from 'node-html-parser'
import { compile } from 'pug'
import { Plugin } from '@client/model'
import uuidv4 from 'uuid'

/**
 * 
 * @param template 
 * @param lang 
 */
const compileTemplate = async (templateTag: HTMLElement, lang: 'html' | 'pug'): Promise<string> => {
  if (lang === 'html') {
    const content = templateTag.querySelector('div')
    return content.toString()
  } else {
    try {
      const fn = compile(templateTag.toString())
      return fn()
    }
     catch (error) {
       throw error
     }
  }
}

/**
 * 
 * @param script 
 * @param lang 
 */
const compileScript = async (script: string, lang: 'js' | 'ts'): Promise<string> => {
  if (lang === 'js') {
    return script
  } else {
    const js = compileString(
      script,
      '', // '--project ./../../tsconfig.json',
      null,
      (error: any) => {
        if (error) {
          throw error.formattedMessage
        }
      }
    )
    return js
  }
}

/**
 * 
 * @param iplRawString 
 */
export const compilePlugin = async (iplRawString: string): Promise<Plugin> => {
  try {
    const plugin = parse(iplRawString, { script: true })
    const elements: HTMLElement[] = plugin.childNodes
      .filter((node): node is HTMLElement => node.nodeType === NodeType.ELEMENT_NODE)

    for (const element of elements) {
      console.log(element.structure)
    }

    // find <template> ? </template>
    const templateTag = elements.find(element => 
      element.tagName === 'template'
    )

    if (!templateTag) {
      throw '[Plugin Compiler] テンプレートが見つかりません'
    }

    const templateLang = templateTag.attributes['lang'] || 'html'
    console.log(`template: ${templateLang}`)
    if (!['html', 'pug'].includes(templateLang)) {
      throw '[Plugin Compiler] 言語が不正です'
    }

    const template = await compileTemplate(templateTag, templateLang as 'html' | 'pug')

    const scriptTag = elements.find(element =>
      element.tagName === 'script'  
    )

    if (!scriptTag) {
      throw '[Plugin Compiler] スクリプトが見つかりません'
    }

    // now support js(default), ts
    const scriptLang = scriptTag.attributes['lang'] || 'js'
    console.log(`script: ${scriptLang}`)
    if (!['js', 'ts'].includes(scriptLang)) {
      throw '[Plugin Compiler] 言語が不正です'
    }

    const functions = await compileScript(scriptTag.text, scriptLang as 'js' | 'ts')

    return { template, functions, instanceId: uuidv4(), config: { enabled: true } }
  } catch (error) {
    console.error(error)
    throw error
  }
}
