"""Converte api.js (com helpers) em SDK literal: avalia os nós com Node e emite node({...}) sem funções."""
import json, subprocess, re, sys, os
src = open(os.path.join(os.path.dirname(__file__), 'api.js')).read()
secret = open('/home/claude/dyno-site/.proxy_secret').read().strip()
src = src.replace('__SEGREDO__', secret)
# Avalia o arquivo com stubs do SDK em Node e coleta nós + conexões
harness = r'''
const EXPR = (s) => ({ __expr: s });
const nodes = []; const conns = [];
function mk(kind, def){ const n = { kind, def, name: def.config.name, outs: {} }; nodes.push(n);
  n.to = (t) => { conns.push([n.name, 0, t.__first ? t.__first.name : t.name]); return t.__last ? t.__last : t; };
  n.onTrue = (t) => { conns.push([n.name, 0, (t.__first||t).name]); return n; };
  n.onFalse = (t) => { conns.push([n.name, 1, (t.__first||t).name]); return n; };
  n.onCase = (i, t) => { conns.push([n.name, i, (t.__first||t).name]); return n; };
  return n; }
// to() precisa devolver um "encadeamento" cujo primeiro nó é o alvo de quem conecta
function wrap(n){ const orig = n.to; n.to = (t) => { const first = n.__first || n; const r = orig(t); return { __first: first, __last: r.__last || r, name: first.name, to: (u) => { const x = (r.__last||r).to(u); return { __first: first, __last: x.__last||x, name: first.name, to: arguments.callee } } } }; return n; }
'''
# Abordagem mais simples: não reimplementar o SDK; gerar à mão abaixo.
