import { chmodSync, readFileSync, writeFileSync } from 'node:fs'

function getFlag(path) {
  const content = readFileSync(path, 'utf8')
  writeFileSync(path, 'flag{no_flag_here}')
  return content
}

const flag0 = getFlag('/flag_0')
const flag1 = getFlag('/flag_1')
const flag2 = getFlag('/flag_2')

let profile = readFileSync('/app/profiles/flag.yml', 'utf8')
profile = profile.replace('flag{test}', flag0)
writeFileSync('/app/profiles/flag.yml', profile)

writeFileSync('/flag_easy', flag1)
chmodSync('/flag_easy', 0o666)

writeFileSync('/flag', flag2)
chmodSync('/flag', 0o400)
